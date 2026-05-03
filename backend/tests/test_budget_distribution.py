def test_distribution_empty_year(client):
    r = client.get("/budget/distribution", params={"year": 2026})
    assert r.status_code == 200
    assert r.json() == {"year": 2026, "months": []}


def test_distribution_all_years_when_no_year_param(client):
    r = client.get("/budget/distribution")
    assert r.status_code == 200
    assert r.json() == {"year": None, "months": []}


def test_distribution_all_years_merges_across_years(client):
    client.post("/budget/incomes", json={"payout_date": "2025-12-31", "amount": 1000})
    client.post("/budget/incomes", json={"payout_date": "2026-01-05", "amount": 2000})
    r = client.get("/budget/distribution")
    assert r.status_code == 200
    body = r.json()
    assert body["year"] is None
    assert len(body["months"]) == 2
    assert body["months"][0]["year"] == 2026 and body["months"][0]["month"] == 1
    assert body["months"][1]["year"] == 2025 and body["months"][1]["month"] == 12


def test_distribution_groups_by_calendar_month(client):
    client.post("/budget/incomes", json={"payout_date": "2026-05-15", "amount": 150000})
    client.post("/budget/incomes", json={"payout_date": "2026-05-30", "amount": 80000})
    client.post("/budget/incomes", json={"payout_date": "2026-06-01", "amount": 1000})
    r = client.get("/budget/distribution", params={"year": 2026})
    assert r.status_code == 200
    body = r.json()
    assert body["year"] == 2026
    assert len(body["months"]) == 2
    # новые месяцы первыми
    assert body["months"][0]["month"] == 6
    assert len(body["months"][0]["incomes"]) == 1
    assert body["months"][1]["month"] == 5
    assert len(body["months"][1]["incomes"]) == 2


def test_income_crud(client):
    r = client.post("/budget/incomes", json={"payout_date": "2026-04-10", "amount": 99000})
    assert r.status_code == 201
    inc = r.json()
    assert inc["amount"] == 99000
    assert inc["items"] == []

    iid = inc["id"]
    r = client.patch(f"/budget/incomes/{iid}", json={"amount": 100000})
    assert r.status_code == 200
    assert r.json()["amount"] == 100000

    r = client.delete(f"/budget/incomes/{iid}")
    assert r.status_code == 204
    assert client.get("/budget/distribution", params={"year": 2026}).json()["months"] == []


def test_create_income_with_category_ids_adds_distribution_rows(client):
    b = client.post(
        "/budget/categories", json={"name": "Бета", "type": "beta", "base_amount": 200}
    ).json()
    a = client.post(
        "/budget/categories", json={"name": "Альфа", "type": "alpha", "base_amount": 100}
    ).json()
    client.post("/budget/categories", json={"name": "Без базы", "type": "none"})

    income = client.post(
        "/budget/incomes",
        json={"payout_date": "2026-09-10", "amount": 300000, "category_ids": [a["id"], b["id"]]},
    ).json()
    assert len(income["items"]) == 2
    assert [i["category_name"] for i in income["items"]] == ["Альфа", "Бета"]
    assert [i["amount"] for i in income["items"]] == [100, 200]
    assert all(i["is_paid"] is False for i in income["items"])


def test_create_income_unknown_category_id(client):
    r = client.post(
        "/budget/incomes",
        json={"payout_date": "2026-09-11", "amount": 1000, "category_ids": [99999]},
    )
    assert r.status_code == 404
    assert r.json()["code"] == "NOT_FOUND"


def test_create_income_category_without_base_amount(client):
    cat = client.post(
        "/budget/categories", json={"name": "Пустая база", "type": "empty_base"}
    ).json()
    r = client.post(
        "/budget/incomes",
        json={"payout_date": "2026-09-12", "amount": 1000, "category_ids": [cat["id"]]},
    )
    assert r.status_code == 422
    assert r.json()["code"] == "HTTP_422"


def test_item_create_uses_category_base_amount(client):
    income = client.post(
        "/budget/incomes", json={"payout_date": "2026-03-01", "amount": 50000}
    ).json()
    assert income["items"] == []
    cat = client.post(
        "/budget/categories", json={"name": "Еда", "type": "food", "base_amount": 12000}
    ).json()
    r = client.post("/budget/items", json={"income_id": income["id"], "category_id": cat["id"]})
    assert r.status_code == 201
    assert r.json()["amount"] == 12000


def test_item_create_requires_amount_when_no_base(client):
    cat = client.post("/budget/categories", json={"name": "Прочее", "type": "misc"}).json()
    income = client.post(
        "/budget/incomes", json={"payout_date": "2026-03-02", "amount": 50000}
    ).json()
    r = client.post("/budget/items", json={"income_id": income["id"], "category_id": cat["id"]})
    assert r.status_code == 422
    assert r.json()["code"] == "HTTP_422"


def test_item_create_income_not_found(client):
    cat = client.post(
        "/budget/categories", json={"name": "Еда", "type": "food2", "base_amount": 1000}
    ).json()
    r = client.post("/budget/items", json={"income_id": 999999, "category_id": cat["id"]})
    assert r.status_code == 404


def test_item_patch_and_delete(client):
    cat = client.post(
        "/budget/categories", json={"name": "ЖКХ", "type": "util", "base_amount": 5000}
    ).json()
    income = client.post(
        "/budget/incomes", json={"payout_date": "2026-07-20", "amount": 90000}
    ).json()
    assert income["items"] == []
    created = client.post(
        "/budget/items",
        json={
            "income_id": income["id"],
            "category_id": cat["id"],
            "amount": 5000,
            "comment": "тест",
        },
    ).json()
    assert created["category_id"] == cat["id"]

    rid = created["id"]
    r = client.patch(f"/budget/items/{rid}", json={"is_paid": True, "amount": 4800})
    assert r.status_code == 200
    assert r.json()["is_paid"] is True
    assert r.json()["amount"] == 4800

    r = client.delete(f"/budget/items/{rid}")
    assert r.status_code == 204

    dist = client.get("/budget/distribution", params={"year": 2026}).json()
    month = next(m for m in dist["months"] if m["month"] == 7)
    row = month["incomes"][0]["items"]
    assert row == []


def test_delete_income_cascades_items(client):
    cat = client.post(
        "/budget/categories", json={"name": "Аренда", "type": "rent2", "base_amount": 10000}
    ).json()
    income = client.post(
        "/budget/incomes", json={"payout_date": "2026-08-01", "amount": 90000}
    ).json()
    client.post("/budget/items", json={"income_id": income["id"], "category_id": cat["id"]})
    client.delete(f"/budget/incomes/{income['id']}")
    d = client.get("/budget/distribution", params={"year": 2026}).json()
    assert not any(m["month"] == 8 for m in d["months"])
