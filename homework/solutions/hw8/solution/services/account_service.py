from solution.repository.base_repository import BaseRepository
from solution.models.account import Account
from typing import List


class AccountService:

    def __init__(self, account_repository: BaseRepository[Account]) -> None:
        self.account_repository = account_repository

    def get_account(self, account_id: int) -> Account:
        return self.account_repository.get(account_id)

    def get_all_accounts(self) -> List[Account]:
        return self.account_repository.get_all()

    def add_account(self, account: Account) -> Account:
        self._validate_account(account)
        self._check_existing_accounts(account)
        return self.account_repository.create(account)

    def update_account(self, account: Account) -> Account:

        self._validate_account(account)
        self._check_existing_accounts(account)
        self.account_repository.get(account.id)
        return self.account_repository.update(account)

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
            if existing.name == account.name and existing.id != account.id:
                raise ValueError("Account name already exists")
