def test_list_categories_empty(client):
    r = client.get("/budget/categories")
    assert r.status_code == 200
    assert r.json() == []


def test_create_category(client):
    r = client.post(
        "/budget/categories", json={"name": "Аренда", "type": "rent", "base_amount": 50000}
    )
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Аренда"
    assert data["type"] == "rent"
    assert data["base_amount"] == 50000
    assert "id" in data


def test_create_category_without_base_amount(client):
    r = client.post("/budget/categories", json={"name": "Аренда", "type": "rent"})
    assert r.status_code == 201
    assert r.json()["base_amount"] is None


def test_create_category_duplicate_type(client):
    client.post("/budget/categories", json={"name": "Аренда", "type": "rent"})
    r = client.post("/budget/categories", json={"name": "Другая", "type": "rent"})
    assert r.status_code == 409
    body = r.json()
    assert body["status"] == "error"
    assert body["code"] == "DUPLICATE_TYPE"


def test_create_category_duplicate_name(client):
    client.post("/budget/categories", json={"name": "Аренда", "type": "rent"})
    r = client.post("/budget/categories", json={"name": "Аренда", "type": "food"})
    assert r.status_code == 409
    body = r.json()
    assert body["status"] == "error"
    assert body["code"] == "DUPLICATE_NAME"


def test_list_categories_sorted_by_name(client):
    client.post("/budget/categories", json={"name": "Транспорт", "type": "transport"})
    client.post("/budget/categories", json={"name": "Аренда", "type": "rent"})
    r = client.get("/budget/categories")
    names = [c["name"] for c in r.json()]
    assert names == sorted(names)


def test_update_category_name(client):
    created = client.post("/budget/categories", json={"name": "Аренда", "type": "rent"}).json()
    r = client.patch(f"/budget/categories/{created['id']}/name", json={"name": "Ипотека"})
    assert r.status_code == 200
    assert r.json()["name"] == "Ипотека"


def test_update_category_name_duplicate(client):
    client.post("/budget/categories", json={"name": "Аренда", "type": "rent"})
    c2 = client.post("/budget/categories", json={"name": "Еда", "type": "food"}).json()
    r = client.patch(f"/budget/categories/{c2['id']}/name", json={"name": "Аренда"})
    assert r.status_code == 409
    assert r.json()["code"] == "DUPLICATE_NAME"


def test_update_category_name_not_found(client):
    r = client.patch("/budget/categories/999/name", json={"name": "Новое"})
    assert r.status_code == 404
    assert r.json()["code"] == "NOT_FOUND"


def test_update_base_amount(client):
    created = client.post(
        "/budget/categories", json={"name": "Аренда", "type": "rent", "base_amount": 50000}
    ).json()
    r = client.patch(f"/budget/categories/{created['id']}/base_amount", json={"base_amount": 60000})
    assert r.status_code == 200
    assert r.json()["base_amount"] == 60000


def test_update_base_amount_to_null(client):
    created = client.post(
        "/budget/categories", json={"name": "Аренда", "type": "rent", "base_amount": 50000}
    ).json()
    r = client.patch(f"/budget/categories/{created['id']}/base_amount", json={"base_amount": None})
    assert r.status_code == 200
    assert r.json()["base_amount"] is None


def test_update_base_amount_not_found(client):
    r = client.patch("/budget/categories/999/base_amount", json={"base_amount": 1000})
    assert r.status_code == 404
    assert r.json()["code"] == "NOT_FOUND"


def test_delete_category(client):
    created = client.post("/budget/categories", json={"name": "Аренда", "type": "rent"}).json()
    r = client.delete(f"/budget/categories/{created['id']}")
    assert r.status_code == 204
    remaining = client.get("/budget/categories").json()
    assert all(c["id"] != created["id"] for c in remaining)


def test_delete_category_not_found(client):
    r = client.delete("/budget/categories/999")
    assert r.status_code == 404
    assert r.json()["code"] == "NOT_FOUND"


def test_update_color(client):
    created = client.post("/budget/categories", json={"name": "Аренда", "type": "rent"}).json()
    r = client.patch(f"/budget/categories/{created['id']}/color", json={"color": "#ef4444"})
    assert r.status_code == 200
    assert r.json()["color"] == "#ef4444"


def test_update_color_to_null(client):
    created = client.post("/budget/categories", json={"name": "Аренда", "type": "rent"}).json()
    client.patch(f"/budget/categories/{created['id']}/color", json={"color": "#ef4444"})
    r = client.patch(f"/budget/categories/{created['id']}/color", json={"color": None})
    assert r.status_code == 200
    assert r.json()["color"] is None


def test_update_color_not_found(client):
    r = client.patch("/budget/categories/999/color", json={"color": "#ef4444"})
    assert r.status_code == 404
    assert r.json()["code"] == "NOT_FOUND"
