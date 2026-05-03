from datetime import date
from typing import List, Literal

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
  status: Literal["error"] = "error"
  code: str
  message: str


class BudgetCategoryOut(BaseModel):
  id: int
  name: str
  type: str
  base_amount: int | None = None
  color: str | None = None

  class Config:
    from_attributes = True


class BudgetCategoryCreate(BaseModel):
  name: str
  type: str
  base_amount: int | None = None


class BudgetCategoryUpdateName(BaseModel):
  name: str


class BudgetCategoryUpdateBaseAmount(BaseModel):
  base_amount: int | None


class BudgetCategoryUpdateColor(BaseModel):
  color: str | None


class BudgetIncomeCreate(BaseModel):
  payout_date: date
  amount: int
  category_ids: List[int] = Field(default_factory=list)


class BudgetItemOut(BaseModel):
  id: int
  income_id: int
  category_id: int
  category_name: str
  amount: int
  comment: str | None = None
  is_paid: bool
  sort_order: int | None = None


class BudgetIncomeOut(BaseModel):
  id: int
  payout_date: date
  amount: int
  items: List[BudgetItemOut]


class BudgetCalendarMonthOut(BaseModel):
  year: int
  month: int
  incomes: List[BudgetIncomeOut]


class BudgetDistributionOut(BaseModel):
  year: int | None = None
  months: List[BudgetCalendarMonthOut]


class BudgetItemCreate(BaseModel):
  income_id: int
  category_id: int
  amount: int | None = None
  comment: str | None = None
  is_paid: bool = False
  sort_order: int | None = None


class BudgetItemUpdate(BaseModel):
  category_id: int | None = None
  amount: int | None = None
  comment: str | None = None
  is_paid: bool | None = None
  sort_order: int | None = None


class SavingGoalHistoryEntry(BaseModel):
    id: str
    date: date
    amount: int
    comment: str | None = None
    is_planned: bool = False
    deletable: bool = False


class SavingGoalOut(BaseModel):
    id: int
    title: str
    comment: str | None = None
    target_amount: int
    currency: str
    initial_amount: int
    category_id: int | None
    category_name: str | None
    milestones: list[int]
    current: int
    percent: int
    history: list[SavingGoalHistoryEntry]

    class Config:
        from_attributes = True


class SavingGoalCreate(BaseModel):
    title: str
    comment: str | None = None
    target_amount: int = 0
    currency: str = "₽"
    initial_amount: int = 0
    category_id: int | None = None
    milestones: list[int] = []


class SavingEntryCreate(BaseModel):
    amount: int
    comment: str | None = None
    date: date


class SavingEntryOut(BaseModel):
    id: int
    goal_id: int
    amount: int
    comment: str | None = None
    date: date
    is_planned: bool

    class Config:
        from_attributes = True
