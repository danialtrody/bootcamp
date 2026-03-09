from solution.repository.base_repository import BaseRepository
from solution.models.account import Account
from solution.models.transaction import Transaction
from solution.models.transfer import Transfer
from typing import List
from decimal import Decimal


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

    def get_account(self, account_id) -> Account:
        return self.account_repository.get(account_id)

    def get_all_accounts(self) -> List[Account]:
        return self.account_repository.get_all()

    def get_account_balance(self, account_id: int) -> Decimal:
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

    def add_account(self, account: Account) -> Account:
        self._validate_account(account)
        self._check_existing_accounts(account)
        return self.account_repository.create(account)

    def update_account_name(self, account_id: int, updated_name: str) -> Account:
        account = self.account_repository.get(account_id)

        new_account = Account(
            id=account.id,
            name=updated_name,
            opening_balance=account.opening_balance,
        )

        self._validate_account(new_account)
        self._check_existing_accounts(new_account)

        return self.account_repository.update(new_account)

    def delete_account(self, account_id: int) -> None:
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
