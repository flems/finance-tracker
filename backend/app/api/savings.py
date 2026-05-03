from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db import get_db
from app.errors import AppError
from app.models import BudgetCategory, BudgetIncome, BudgetItem, SavingEntry, SavingGoal
from app.schemas import (
    SavingEntryCreate,
    SavingEntryOut,
    SavingGoalCreate,
    SavingGoalHistoryEntry,
    SavingGoalOut,
)

router = APIRouter(prefix="/savings", tags=["savings"])

BudgetRow = tuple[BudgetItem, date]


def _build_goal_out(
    goal: SavingGoal,
    budget_rows: list[BudgetRow],
    entries: list[SavingEntry],
) -> SavingGoalOut:
    today = date.today()

    history: list[SavingGoalHistoryEntry] = []

    for item, payout_date in budget_rows:
        history.append(
            SavingGoalHistoryEntry(
                id=f"item-{item.id}",
                date=payout_date,
                amount=item.amount,
                comment=item.comment,
                is_planned=payout_date > today,
                deletable=False,
            )
        )

    for entry in entries:
        history.append(
            SavingGoalHistoryEntry(
                id=f"entry-{entry.id}",
                date=entry.date,
                amount=entry.amount,
                comment=entry.comment,
                is_planned=entry.date > today,
                deletable=True,
            )
        )

    history.sort(key=lambda h: h.date)

    current = goal.initial_amount + sum(h.amount for h in history if not h.is_planned)
    percent = min(100, round(current / goal.target_amount * 100)) if goal.target_amount > 0 else 0

    return SavingGoalOut(
        id=goal.id,
        title=goal.title,
        comment=goal.comment,
        target_amount=goal.target_amount,
        currency=goal.currency,
        initial_amount=goal.initial_amount,
        category_id=goal.category_id,
        category_name=goal.category.name if goal.category else None,
        milestones=goal.milestones or [],
        current=current,
        percent=percent,
        history=history,
    )


def _fetch_budget_rows(db: Session, category_id: int) -> list[BudgetRow]:
    return db.execute(
        select(BudgetItem, BudgetIncome.payout_date)
        .join(BudgetIncome, BudgetItem.income_id == BudgetIncome.id)
        .where(BudgetItem.category_id == category_id)
        .order_by(BudgetIncome.payout_date)
    ).all()


@router.get("/goals", response_model=list[SavingGoalOut])
def get_saving_goals(db: Session = Depends(get_db)):
    goals = (
        db.execute(
            select(SavingGoal)
            .options(selectinload(SavingGoal.category), selectinload(SavingGoal.entries))
            .order_by(SavingGoal.id)
        )
        .scalars()
        .all()
    )

    return [
        _build_goal_out(
            goal,
            _fetch_budget_rows(db, goal.category_id) if goal.category_id is not None else [],
            list(goal.entries),
        )
        for goal in goals
    ]


@router.post("/goals", response_model=SavingGoalOut, status_code=201)
def create_saving_goal(body: SavingGoalCreate, db: Session = Depends(get_db)):
    cat = None
    if body.category_id is not None:
        cat = db.get(BudgetCategory, body.category_id)
        if not cat:
            raise AppError(404, "NOT_FOUND", "Категория не найдена")

    goal = SavingGoal(
        title=body.title,
        comment=body.comment,
        target_amount=body.target_amount,
        currency=body.currency,
        initial_amount=body.initial_amount,
        category_id=body.category_id,
        milestones=body.milestones,
    )
    goal.category = cat
    db.add(goal)
    db.commit()
    db.refresh(goal)

    return _build_goal_out(goal, [], [])


@router.delete("/goals/{goal_id}", status_code=204)
def delete_saving_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.get(SavingGoal, goal_id)
    if not goal:
        raise AppError(404, "NOT_FOUND", "Цель накопления не найдена")
    db.delete(goal)
    db.commit()


@router.delete("/entries/{entry_id}", status_code=204)
def delete_saving_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.get(SavingEntry, entry_id)
    if not entry:
        raise AppError(404, "NOT_FOUND", "Запись не найдена")
    db.delete(entry)
    db.commit()


@router.post("/goals/{goal_id}/entries", response_model=SavingEntryOut, status_code=201)
def create_saving_entry(goal_id: int, body: SavingEntryCreate, db: Session = Depends(get_db)):
    goal = db.get(SavingGoal, goal_id)
    if not goal:
        raise AppError(404, "NOT_FOUND", "Цель накопления не найдена")

    entry = SavingEntry(
        goal_id=goal_id,
        amount=body.amount,
        comment=body.comment,
        date=body.date,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)

    return SavingEntryOut(
        id=entry.id,
        goal_id=entry.goal_id,
        amount=entry.amount,
        comment=entry.comment,
        date=entry.date,
        is_planned=entry.date > date.today(),
    )
