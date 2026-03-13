from solution.repository.base_repository import BaseRepository
from solution.models.account import Account
from solution.models.transaction import Transaction
from solution.models.transfer import Transfer
from decimal import Decimal


class NetWorth:

    def __init__(
        self,
        account_repository: BaseRepository[Account],
        transaction_repository: BaseRepository[Transaction],
        transfer_repository: BaseRepository[Transfer],
    ) -> None:
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository
        self.transfer_repository = transfer_repository

    async def calculate_net_worth(self) -> Decimal:

        net_worth = Decimal("0")

        accounts = self.account_repository.get_all()
        transactions = self.transaction_repository.get_all()

        for account in accounts:
            balance = account.opening_balance
            for transaction in transactions:
                if transaction.account_id == account.id:
                    if transaction.type == "income":
                        balance += transaction.amount
                    elif transaction.type == "expense":
                        balance -= transaction.amount

            net_worth += balance

        return net_worth
