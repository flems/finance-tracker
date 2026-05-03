from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.db import get_db
from app.errors import AppError
from app.models import BudgetCategory, BudgetIncome, BudgetItem
from app.schemas import (
  BudgetCalendarMonthOut,
  BudgetCategoryCreate,
  BudgetCategoryOut,
  BudgetCategoryUpdateBaseAmount,
  BudgetCategoryUpdateColor,
  BudgetCategoryUpdateName,
  BudgetDistributionOut,
  BudgetIncomeCreate,
  BudgetIncomeOut,
  BudgetItemCreate,
  BudgetItemOut,
  BudgetItemUpdate,
)

router = APIRouter(prefix="/budget", tags=["budget"])


def _utcnow() -> datetime:
  return datetime.now(timezone.utc)


def _category_map(db: Session) -> dict[int, BudgetCategory]:
  rows = db.execute(select(BudgetCategory)).scalars().all()
  return {c.id: c for c in rows}


def _sorted_items_for_income(items: list[BudgetItem], cat_by_id: dict[int, BudgetCategory]) -> list[BudgetItemOut]:
  ordered = sorted(items, key=lambda i: (i.sort_order is None, i.sort_order if i.sort_order is not None else 0, i.id))
  return [
    BudgetItemOut(
      id=i.id,
      income_id=i.income_id,
      category_id=i.category_id,
      category_name=cat_by_id[i.category_id].name,
      amount=i.amount,
      comment=i.comment,
      is_paid=i.is_paid,
      sort_order=i.sort_order,
    )
    for i in ordered
  ]


@router.get("/distribution", response_model=BudgetDistributionOut)
def get_distribution(year: int | None = Query(default=None, ge=2000, le=2100), db: Session = Depends(get_db)):
  q = select(BudgetIncome).options(selectinload(BudgetIncome.items)).order_by(BudgetIncome.payout_date)
  if year is not None:
    start = date(year, 1, 1)
    end = date(year, 12, 31)
    q = q.where(BudgetIncome.payout_date >= start, BudgetIncome.payout_date <= end)
  incomes = db.execute(q).scalars().all()
  cat_by_id = _category_map(db)
  by_month: dict[tuple[int, int], list[BudgetIncome]] = {}
  for inc in incomes:
    key = (inc.payout_date.year, inc.payout_date.month)
    by_month.setdefault(key, []).append(inc)
  months_out: list[BudgetCalendarMonthOut] = []
  for y, m in sorted(by_month.keys(), reverse=True):
    month_incomes = [
      BudgetIncomeOut(
        id=inc.id,
        payout_date=inc.payout_date,
        amount=inc.amount,
        items=_sorted_items_for_income(list(inc.items), cat_by_id),
      )
      for inc in sorted(by_month[(y, m)], key=lambda i: (i.payout_date, i.id))
    ]
    months_out.append(BudgetCalendarMonthOut(year=y, month=m, incomes=month_incomes))
  return BudgetDistributionOut(year=year, months=months_out)


def _unique_ids_preserve_order(ids: list[int]) -> list[int]:
  seen: set[int] = set()
  out: list[int] = []
  for i in ids:
    if i in seen:
      continue
    seen.add(i)
    out.append(i)
  return out


@router.post("/incomes", response_model=BudgetIncomeOut, status_code=201)
def create_income(body: BudgetIncomeCreate, db: Session = Depends(get_db)):
  category_ids = _unique_ids_preserve_order(body.category_ids)
  resolved_lines: list[tuple[int, int]] = []
  for cid in category_ids:
    category = db.get(BudgetCategory, cid)
    if not category:
      raise AppError(404, "NOT_FOUND", "Категория не найдена")
    if category.base_amount is None:
      raise AppError(422, "HTTP_422", "У выбранной категории нет базовой суммы — укажите её в категории или добавьте строку вручную")
    resolved_lines.append((cid, category.base_amount))

  income = BudgetIncome(payout_date=body.payout_date, amount=body.amount)
  db.add(income)
  db.flush()

  for sort_order, (cid, amount) in enumerate(resolved_lines):
    db.add(
      BudgetItem(
        income_id=income.id,
        category_id=cid,
        amount=amount,
        comment=None,
        is_paid=False,
        sort_order=sort_order,
      ),
    )

  db.commit()

  income_loaded = db.execute(
    select(BudgetIncome).where(BudgetIncome.id == income.id).options(selectinload(BudgetIncome.items)),
  ).scalars().one()

  cat_by_id = _category_map(db)
  return BudgetIncomeOut(
    id=income_loaded.id,
    payout_date=income_loaded.payout_date,
    amount=income_loaded.amount,
    items=_sorted_items_for_income(list(income_loaded.items), cat_by_id),
  )


@router.delete("/incomes/{income_id}", status_code=204)
def delete_income(income_id: int, db: Session = Depends(get_db)):
  income = db.get(BudgetIncome, income_id)
  if not income:
    raise AppError(404, "NOT_FOUND", "Выплата не найдена")
  db.delete(income)
  db.commit()


def _next_item_sort_order(db: Session, income_id: int) -> int | None:
  m = db.execute(select(func.max(BudgetItem.sort_order)).where(BudgetItem.income_id == income_id)).scalar_one()
  if m is None:
    return 0
  return int(m) + 1


@router.post("/items", response_model=BudgetItemOut, status_code=201)
def create_item(body: BudgetItemCreate, db: Session = Depends(get_db)):
  income = db.get(BudgetIncome, body.income_id)
  if not income:
    raise AppError(404, "NOT_FOUND", "Выплата не найдена")
  category = db.get(BudgetCategory, body.category_id)
  if not category:
    raise AppError(404, "NOT_FOUND", "Категория не найдена")
  amount = body.amount if body.amount is not None else category.base_amount
  if amount is None:
    raise AppError(422, "HTTP_422", "Задайте сумму или базовую сумму категории")
  sort_order = body.sort_order if body.sort_order is not None else _next_item_sort_order(db, body.income_id)
  row = BudgetItem(
    income_id=body.income_id,
    category_id=body.category_id,
    amount=amount,
    comment=body.comment,
    is_paid=body.is_paid,
    sort_order=sort_order,
  )
  db.add(row)
  db.commit()
  db.refresh(row)
  cat_by_id = _category_map(db)
  r = row
  return BudgetItemOut(
    id=r.id,
    income_id=r.income_id,
    category_id=r.category_id,
    category_name=cat_by_id[r.category_id].name,
    amount=r.amount,
    comment=r.comment,
    is_paid=r.is_paid,
    sort_order=r.sort_order,
  )


@router.patch("/items/{item_id}", response_model=BudgetItemOut)
def update_item(item_id: int, body: BudgetItemUpdate, db: Session = Depends(get_db)):
  row = db.get(BudgetItem, item_id)
  if not row:
    raise AppError(404, "NOT_FOUND", "Строка бюджета не найдена")
  if body.category_id is not None:
    category = db.get(BudgetCategory, body.category_id)
    if not category:
      raise AppError(404, "NOT_FOUND", "Категория не найдена")
    row.category_id = body.category_id
  if body.amount is not None:
    row.amount = body.amount
  if body.comment is not None:
    row.comment = body.comment
  if body.is_paid is not None:
    row.is_paid = body.is_paid
  if body.sort_order is not None:
    row.sort_order = body.sort_order
  row.updated_at = _utcnow()
  db.commit()
  db.refresh(row)
  cat_by_id = _category_map(db)
  r = row
  return BudgetItemOut(
    id=r.id,
    income_id=r.income_id,
    category_id=r.category_id,
    category_name=cat_by_id[r.category_id].name,
    amount=r.amount,
    comment=r.comment,
    is_paid=r.is_paid,
    sort_order=r.sort_order,
  )


@router.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
  row = db.get(BudgetItem, item_id)
  if not row:
    raise AppError(404, "NOT_FOUND", "Строка бюджета не найдена")
  db.delete(row)
  db.commit()


@router.get("/categories", response_model=list[BudgetCategoryOut])
def list_categories(db: Session = Depends(get_db)):
  return db.execute(select(BudgetCategory).order_by(BudgetCategory.name)).scalars().all()


@router.post("/categories", response_model=BudgetCategoryOut, status_code=201)
def create_category(body: BudgetCategoryCreate, db: Session = Depends(get_db)):
  if body.type and db.execute(select(BudgetCategory).where(BudgetCategory.type == body.type)).first():
    raise AppError(409, "DUPLICATE_TYPE", "Категория с таким типом уже существует")
  if db.execute(select(BudgetCategory).where(BudgetCategory.name == body.name)).first():
    raise AppError(409, "DUPLICATE_NAME", "Категория с таким названием уже существует")
  category = BudgetCategory(**body.model_dump())
  db.add(category)
  db.commit()
  db.refresh(category)
  return category


@router.patch("/categories/{category_id}/name", response_model=BudgetCategoryOut)
def update_category_name(category_id: int, body: BudgetCategoryUpdateName, db: Session = Depends(get_db)):
  category = db.get(BudgetCategory, category_id)
  if not category:
    raise AppError(404, "NOT_FOUND", "Категория не найдена")
  if db.execute(select(BudgetCategory).where(BudgetCategory.name == body.name, BudgetCategory.id != category_id)).first():
    raise AppError(409, "DUPLICATE_NAME", "Категория с таким названием уже существует")
  category.name = body.name
  db.commit()
  db.refresh(category)
  return category


@router.delete("/categories/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)):
  category = db.get(BudgetCategory, category_id)
  if not category:
    raise AppError(404, "NOT_FOUND", "Категория не найдена")
  db.delete(category)
  db.commit()


@router.patch("/categories/{category_id}/base_amount", response_model=BudgetCategoryOut)
def update_category_base_amount(category_id: int, body: BudgetCategoryUpdateBaseAmount, db: Session = Depends(get_db)):
  category = db.get(BudgetCategory, category_id)
  if not category:
    raise AppError(404, "NOT_FOUND", "Категория не найдена")
  category.base_amount = body.base_amount
  db.commit()
  db.refresh(category)
  return category


@router.patch("/categories/{category_id}/color", response_model=BudgetCategoryOut)
def update_category_color(category_id: int, body: BudgetCategoryUpdateColor, db: Session = Depends(get_db)):
  category = db.get(BudgetCategory, category_id)
  if not category:
    raise AppError(404, "NOT_FOUND", "Категория не найдена")
  category.color = body.color
  db.commit()
  db.refresh(category)
  return category


