import datetime
from decimal import Decimal
from solution.database import Base
from sqlalchemy import DECIMAL, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from solution.models.account import Account


MAX_TRANSFER_DESCRIPTION_LENGTH = 255


class Transfer(Base):
    __tablename__ = "transfers"

    transfer_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    transfer_amount: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)
    transfer_description: Mapped[str] = mapped_column(
        String(MAX_TRANSFER_DESCRIPTION_LENGTH), nullable=False
    )
    transaction_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    from_account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.account_id"), nullable=False
    )
    to_account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.account_id"), nullable=False
    )

    from_account: Mapped["Account"] = relationship(
        "Account", foreign_keys=[from_account_id], back_populates="outgoing_transfers"
    )
    to_account: Mapped["Account"] = relationship(
        "Account", foreign_keys=[to_account_id], back_populates="incoming_transfers"
    )
