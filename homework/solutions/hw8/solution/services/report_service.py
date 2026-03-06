from decimal import Decimal
from solution.repository.base_repository import BaseRepository
from solution.models.transaction import Transaction
from solution.models.categories import Category


class ReportService:

    def __init__(
        self,
        transaction_repository: BaseRepository[Transaction],
        category_repository: BaseRepository[Category],
    ) -> None:

        self.transaction_repository = transaction_repository
        self.category_repository = category_repository

    def get_monthly_summary(
        self, month: int, year: int, account_id: int
    ) -> dict[str, Decimal]:

        total_income = Decimal("0")
        total_expense = Decimal("0")

        for transaction in self.transaction_repository.get_all():

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

    def get_spending_breakdown_by_category(
        self,
        month: int,
        year: int,
        account_id: int,
    ) -> dict[str, Decimal]:

        result: dict[str, Decimal] = {}
        categories = {
            category.id: category.name
            for category in self.category_repository.get_all()
        }

        for transaction in self.transaction_repository.get_all():
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
        account_id: int,
        transaction_type: str | None = None,
    ) -> bool:

        if transaction.date.month != month or transaction.date.year != year:
            return False
        if account_id and transaction.account_id != account_id:
            return False
        if transaction_type and transaction.type != transaction_type:
            return False

        return True
