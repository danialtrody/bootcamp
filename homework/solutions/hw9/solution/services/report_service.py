from decimal import Decimal
from solution.repository.base_repository import BaseRepository
from solution.models.transaction import Transaction
from solution.models.categories import Category
from typing import Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from solution.database import async_session_maker


class ReportService:

    def __init__(
        self,
        transaction_repository: BaseRepository[Transaction],
        category_repository: BaseRepository[Category],
        session_maker: Optional[async_sessionmaker[AsyncSession]] = None,
    ) -> None:

        self.transaction_repository = transaction_repository
        self.category_repository = category_repository
        self.session_maker = session_maker or async_session_maker

    async def get_monthly_summary(
        self,
        month: int,
        year: int,
        account_id: Optional[int] = None,
    ) -> dict[str, Decimal]:

        async with self.session_maker() as session:
            total_income = Decimal("0")
            total_expense = Decimal("0")

            transactions = await self.transaction_repository.get_all(session)

            for transaction in transactions:

                if not self._is_valid_transaction(transaction, month, year, account_id):
                    continue

                if transaction.type == "income":
                    total_income += transaction.amount

                elif transaction.type == "expense":
                    total_expense += transaction.amount

            return {
                "total_income": total_income,
                "total_expense": total_expense,
                "net_cash_flow": total_income - total_expense,
            }

    async def get_spending_breakdown_by_category(
        self,
        month: int,
        year: int,
        account_id: Optional[int] = None,
    ) -> dict[str, Decimal]:

        async with self.session_maker() as session:
            result: Dict[str, Decimal] = {}

            categories = {
                category.id: category.name
                for category in await self.category_repository.get_all(session)
            }

            for transaction in await self.transaction_repository.get_all(session):

                if not self._is_valid_transaction(
                    transaction, month, year, account_id, "expense"
                ):
                    continue

                category_name = categories.get(transaction.category_id, "Unknown")

                result[category_name] = (
                    result.get(category_name, Decimal("0")) + transaction.amount
                )

            return result

    def _is_valid_transaction(
        self,
        transaction: Transaction,
        month: int,
        year: int,
        account_id: Optional[int] = None,
        transaction_type: Optional[str] = None,
    ) -> bool:

        if transaction.date.month != month or transaction.date.year != year:
            return False

        if account_id is not None and transaction.account_id != account_id:
            return False

        if transaction_type is not None and transaction.type != transaction_type:
            return False

        return True
