from decimal import Decimal
from solution.database import Base
from sqlalchemy import DECIMAL, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from solution.models.transaction import Transaction
    from solution.models.transfer import Transfer


MAX_ACCOUNT_NAME_LENGTH = 255


class Account(Base):
    __tablename__ = "accounts"

    account_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    account_name: Mapped[str] = mapped_column(
        String(MAX_ACCOUNT_NAME_LENGTH), nullable=False
    )
    opening_balance: Mapped[Decimal] = mapped_column(
        DECIMAL, default=Decimal("0"), nullable=False
    )

    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="account"
    )

    outgoing_transfers: Mapped[list["Transfer"]] = relationship(
        "Transfer",
        foreign_keys="[Transfer.from_account_id]",
        back_populates="from_account",
    )
    incoming_transfers: Mapped[list["Transfer"]] = relationship(
        "Transfer", foreign_keys="[Transfer.to_account_id]", back_populates="to_account"
    )
