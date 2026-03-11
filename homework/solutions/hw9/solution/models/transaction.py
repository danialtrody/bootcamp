import datetime
from decimal import Decimal
from solution.database import Base
from sqlalchemy import DECIMAL, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from solution.models.account import Account
    from solution.models.categories import Category

MAX_TRANSACTION_TYPE_LENGTH = 100


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    transaction_amount: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)
    transaction_type: Mapped[str] = mapped_column(
        String(MAX_TRANSACTION_TYPE_LENGTH), nullable=False
    )
    transaction_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.account_id"), nullable=False
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.category_id"), nullable=False
    )

    account: Mapped["Account"] = relationship("Account", back_populates="transactions")
    category: Mapped["Category"] = relationship(
        "Category", back_populates="transactions"
    )
