from solution.repository.base_repository import BaseRepository
from solution.models.account import Account
from solution.models.transaction import Transaction
from solution.models.transfer import Transfer
from decimal import Decimal
from typing import List, Dict, Any


class AccountService:

    def __init__(
        self,
        account_repository: BaseRepository[Account],
        transaction_repository: BaseRepository[Transaction],
        transfer_repository: BaseRepository[Transfer],
    ) -> None:
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository
        self.transfer_repository = transfer_repository

    async def get_account(self, account_id: int) -> dict[Any, Any]:
        account = self.account_repository.get(account_id)
        return account.to_dict()

    async def get_all_accounts(self) -> List[dict[Any, Any]]:
        accounts = self.account_repository.get_all()
        return [account.to_dict() for account in accounts]

    async def get_account_balance(self, account_id: int) -> Decimal:
        account = self.account_repository.get(account_id)

        balance = account.opening_balance

        transactions = self.transaction_repository.get_all()
        for transaction in transactions:
            if transaction.account_id == account_id:
                if transaction.type == "income":
                    balance += transaction.amount
                else:
                    balance -= transaction.amount

        transfers = self.transfer_repository.get_all()
        for transfer in transfers:
            if transfer.from_account_id == account_id:
                balance -= transfer.amount
            if transfer.to_account_id == account_id:
                balance += transfer.amount

        return balance

    async def add_account(self, account_data: Dict[str, Any]) -> Dict[str, Any]:

        account = Account(
            name=account_data["name"], opening_balance=account_data["opening_balance"]
        )

        self._validate_account(account)
        self._check_existing_accounts(account)
        created = self.account_repository.create(account)
        return created.to_dict()

    async def update_account_name(
        self, account_id: int, updated_name: str
    ) -> Dict[str, Any]:
        account = self.account_repository.get(account_id)

        new_account = Account(
            id=account.id,
            name=updated_name,
            opening_balance=account.opening_balance,
        )

        self._validate_account(new_account)
        self._check_existing_accounts(new_account)

        updated = self.account_repository.update(new_account)
        return updated.to_dict()

    async def delete_account(self, account_id: int) -> None:
        self.account_repository.delete(account_id)

    def _validate_account(self, account: Account) -> None:
        if account is None:
            raise ValueError("Account cannot be None")

        if not account.name.strip():
            raise ValueError("Account name cannot be empty")

        if account.opening_balance is None:
            raise ValueError("Account opening balance cannot be empty")

    def _check_existing_accounts(self, account: Account) -> None:
        existing_accounts = self.account_repository.get_all()

        for existing in existing_accounts:
            if (
                existing.name.lower() == account.name.lower() and existing.id != account.id
            ):
                raise ValueError("Account name already exists")
