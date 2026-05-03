from sqlalchemy import (
    JSON,
    TIMESTAMP,
    BigInteger,
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    text,
)
from sqlalchemy.orm import relationship

from .db import Base


class BudgetCategory(Base):
    __tablename__ = "budget_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    type = Column(String(64), unique=True, nullable=False)
    base_amount = Column(Integer)
    color = Column(String(7))


class BudgetIncome(Base):
    __tablename__ = "budget_incomes"

    id = Column(BigInteger, primary_key=True, index=True)
    payout_date = Column(Date, nullable=False, index=True)
    amount = Column(Integer, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    items = relationship("BudgetItem", back_populates="income", cascade="all, delete-orphan")


class BudgetItem(Base):
    __tablename__ = "budget_items"

    id = Column(BigInteger, primary_key=True, index=True)
    income_id = Column(
        BigInteger, ForeignKey("budget_incomes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    category_id = Column(Integer, ForeignKey("budget_categories.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    comment = Column(String)
    is_paid = Column(Boolean, nullable=False, server_default=text("false"))
    sort_order = Column(SmallInteger)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    income = relationship("BudgetIncome", back_populates="items")


class SavingGoal(Base):
    __tablename__ = "saving_goals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    comment = Column(String)
    target_amount = Column(Integer, nullable=False, server_default=text("0"))
    currency = Column(String(16), nullable=False, server_default=text("'₽'"))
    initial_amount = Column(Integer, nullable=False, server_default=text("0"))
    category_id = Column(Integer, ForeignKey("budget_categories.id"), nullable=True)
    milestones = Column(JSON, nullable=False, server_default=text("'[]'::json"))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    category = relationship("BudgetCategory")
    entries = relationship("SavingEntry", back_populates="goal", cascade="all, delete-orphan")


class SavingEntry(Base):
    __tablename__ = "saving_entries"

    id = Column(BigInteger, primary_key=True, index=True)
    goal_id = Column(
        Integer, ForeignKey("saving_goals.id", ondelete="CASCADE"), nullable=False, index=True
    )
    amount = Column(Integer, nullable=False)
    comment = Column(String)
    date = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    goal = relationship("SavingGoal", back_populates="entries")
