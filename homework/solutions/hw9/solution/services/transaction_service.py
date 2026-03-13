from solution.repository.base_repository import BaseRepository
from solution.models.transaction import Transaction
from solution.models.account import Account
from solution.models.categories import Category
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from solution.database import async_session_maker

from typing import List, Any, Optional
from decimal import Decimal
import datetime


def _transaction_to_dict(transaction: Transaction) -> dict[str, Any]:
    return {
        "id": transaction.id,
        "amount": float(transaction.amount),
        "date": transaction.date,
        "type": transaction.type,
        "account_id": transaction.account_id,
        "category_id": transaction.category_id,
    }


class TransactionService:

    def __init__(
        self,
        transaction_repository: BaseRepository[Transaction],
        account_repository: BaseRepository[Account],
        category_repository: BaseRepository[Category],
        session_maker: Optional[async_sessionmaker[AsyncSession]] = None,
    ) -> None:
        self.transaction_repository = transaction_repository
        self.account_repository = account_repository
        self.category_repository = category_repository
        self.session_maker = session_maker or async_session_maker

    async def get_all_transactions(
        self,
        account_id: Optional[int] = None,
        month: Optional[int] = None,
        year: Optional[int] = None,
    ) -> List[dict[Any, Any]]:

        async with self.session_maker() as session:
            transactions = await self.transaction_repository.get_all(session)

            if account_id is not None:
                transactions = [
                    transation
                    for transation in transactions
                    if transation.account_id == account_id
                ]
            if month is not None:
                transactions = [
                    transation
                    for transation in transactions
                    if transation.date.month == month
                ]
            if year is not None:
                transactions = [
                    transation
                    for transation in transactions
                    if transation.date.year == year
                ]

            transaction_to_dict = [
                _transaction_to_dict(transaction) for transaction in transactions
            ]
            return transaction_to_dict

    async def add_income(self, transaction_data: dict[Any, Any]) -> dict[Any, Any]:

        async with self.session_maker() as session:
            async with session.begin():
                transaction = Transaction(
                    amount=Decimal(transaction_data["amount"]),
                    date=transaction_data.get("date", datetime.date.today()),
                    type="income",
                    account_id=transaction_data["account_id"],
                    category_id=transaction_data["category_id"],
                )

                if transaction.amount <= 0:
                    raise ValueError("Income amount must be positive")
                if not await self.account_repository.exists(
                    session, transaction.account_id
                ):
                    raise ValueError(
                        f"Account with ID {transaction.account_id} does not exist"
                    )
                if not await self.category_repository.exists(
                    session, transaction.category_id
                ):
                    raise ValueError(
                        f"Category with ID {transaction.category_id} does not exist"
                    )

                transaction.type = "income"
                created = await self.transaction_repository.create(session, transaction)
            return _transaction_to_dict(created)

    async def add_expense(self, transaction_data: dict[Any, Any]) -> dict[Any, Any]:
        async with self.session_maker() as session:
            async with session.begin():

                transaction = Transaction(
                    amount=Decimal(transaction_data["amount"]),
                    date=transaction_data.get("date", datetime.date.today()),
                    type="expense",
                    account_id=transaction_data["account_id"],
                    category_id=transaction_data["category_id"],
                )

                if transaction.amount <= 0:
                    raise ValueError("Expense amount must be positive")
                if not await self.account_repository.exists(
                    session, transaction.account_id
                ):
                    raise ValueError(
                        f"Account with ID {transaction.account_id} does not exist"
                    )
                if not await self.category_repository.exists(
                    session, transaction.category_id
                ):
                    raise ValueError(
                        f"Category with ID {transaction.category_id} does not exist"
                    )

                transaction.type = "expense"
                created = await self.transaction_repository.create(session, transaction)
            return _transaction_to_dict(created)

    async def delete_transaction(self, transaction_id: int) -> None:
        async with self.session_maker() as session:
            async with session.begin():
                await self.transaction_repository.delete(session, transaction_id)
