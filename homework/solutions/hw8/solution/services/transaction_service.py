from solution.repository.base_repository import BaseRepository
from solution.models.transaction import Transaction
from typing import List
from typing import Optional


class TransactionService:

    def __init__(self, transaction_repository: BaseRepository[Transaction]) -> None:
        self.transaction_repository = transaction_repository

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
        transaction.type = "income"

        return self.transaction_repository.create(transaction)

    def add_expense(self, transaction: Transaction) -> Transaction:
        if transaction.amount <= 0:
            raise ValueError("Expense amount must be positive")
        transaction.type = "expense"

        return self.transaction_repository.create(transaction)

    def delete_transaction(self, transaction_id: int) -> None:
        self.transaction_repository.delete(transaction_id)
