import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect

from app.api.budget import router as budget_router
from app.api.savings import router as savings_router
from app.db import Base, engine
from app.errors import AppError, app_error_handler
import app.models as app_models  # noqa: F401 — регистрирует все модели


def _reset_budget_payroll_tables_if_requested() -> None:
  """Одноразово: затереть строки выплат при смене схемы (см. RESET_BUDGET_SCHEMA)."""
  if os.getenv("RESET_BUDGET_SCHEMA") != "1":
    return
  app_models.BudgetItem.__table__.drop(bind=engine, checkfirst=True)
  app_models.BudgetIncome.__table__.drop(bind=engine, checkfirst=True)


def _should_validate_budget_tables() -> bool:
  """При pytest worker импортит _pytest — проверку dev-БД пропускаем (контуры URL разъехались)."""
  return not any(mod.startswith("_pytest") for mod in sys.modules)


def _ensure_budget_items_schema_or_fail() -> None:
  if not _should_validate_budget_tables():
    return
  inspector = inspect(engine)
  if not inspector.has_table("budget_items"):
    return
  col_names = {c["name"] for c in inspector.get_columns("budget_items")}
  if "income_id" in col_names:
    return
  raise RuntimeError(
    "БД устарела: в таблице budget_items нет колонки income_id. SQLAlchemy create_all() только создаёт "
    "новые таблицы и не меняет уже существующие.\n\n"
    'Исправление (удалятся только выплаты и строки распределения, категории останутся): '
    "docker compose exec db psql -U sport_user -d sport_tracker -c "
    '"DROP TABLE IF EXISTS budget_items CASCADE; DROP TABLE IF EXISTS budget_incomes CASCADE;" '
    "и затем docker compose restart backend.\n\n"
    "Или один раз задайте в environment backend переменную RESET_BUDGET_SCHEMA=1 и перезапустите контейнер, "
    "потом уберите её.",
  )


@asynccontextmanager
async def lifespan(app: FastAPI):
  _reset_budget_payroll_tables_if_requested()
  Base.metadata.create_all(bind=engine)
  _ensure_budget_items_schema_or_fail()
  yield


app = FastAPI(title="Finance Tracker", lifespan=lifespan)

app.add_exception_handler(AppError, app_error_handler)

# CORS: разрешаем запросы с фронта (Vite на 5173 порту)
origins = [
  "http://localhost:5173",
  "http://127.0.0.1:5173",
  "http://localhost:5174",
  "http://127.0.0.1:5174",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


@app.get("/health")
def health_check():
  return {"status": "ok"}


app.include_router(budget_router)
app.include_router(savings_router)

