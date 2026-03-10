from solution.repository.base_repository import BaseRepository
from solution.models.transaction import Transaction
from solution.models.account import Account
from solution.models.categories import Category

from typing import List
from typing import Optional


class TransactionService:

    def __init__(
        self,
        transaction_repository: BaseRepository[Transaction],
        account_repository: BaseRepository[Account],
        category_repository: BaseRepository[Category]
    ) -> None:
        self.transaction_repository = transaction_repository
        self.account_repository = account_repository
        self.category_repository = category_repository

    def get_all_transactions(
        self,
        account_id: Optional[int] = None,
        month: Optional[int] = None,
        year: Optional[int] = None,
    ) -> List[Transaction]:

        transactions = self.transaction_repository.get_all()

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

        return transactions

    def add_income(self, transaction: Transaction) -> Transaction:
        if transaction.amount <= 0:
            raise ValueError("Income amount must be positive")
        if not self.account_repository.exists(transaction.account_id):
            raise ValueError(f"Account with ID {transaction.account_id} does not exist")
        if not self.category_repository.exists(transaction.category_id):
            raise ValueError(f"Category with ID {transaction.category_id} does not exist")

        transaction.type = "income"
        return self.transaction_repository.create(transaction)

    def add_expense(self, transaction: Transaction) -> Transaction:
        if transaction.amount <= 0:
            raise ValueError("Expense amount must be positive")
        if not self.account_repository.exists(transaction.account_id):
            raise ValueError(f"Account with ID {transaction.account_id} does not exist")
        if not self.category_repository.exists(transaction.category_id):
            raise ValueError(f"Category with ID {transaction.category_id} does not exist")

        transaction.type = "expense"
        return self.transaction_repository.create(transaction)

    def delete_transaction(self, transaction_id: int) -> None:
        self.transaction_repository.delete(transaction_id)
