from enum import Enum
from solution.database import Base
from sqlalchemy import Integer, String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from solution.models.transaction import Transaction


MAX_CATEGORY_NAME_LENGTH = 100


class CategoryType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(MAX_CATEGORY_NAME_LENGTH), nullable=False
    )
    type: Mapped[CategoryType] = mapped_column(
        SQLEnum(CategoryType), nullable=False
    )

    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="category"
    )
