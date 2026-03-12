from typing import Any, Optional, List
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession
from solution.database import async_session_maker
from solution.models.account import Account
from solution.models.transaction import Transaction
from solution.models.transfer import Transfer
from solution.repository.base_repository import BaseRepository


def _account_to_dict(account: Account) -> dict[str, Any]:
    return {
        "id": account.id,
        "name": account.name,
        "opening_balance": account.opening_balance,
    }


class AccountService:

    def __init__(
        self,
        account_repo: Optional[BaseRepository[Account]] = None,
        transaction_repo: Optional[BaseRepository[Transaction]] = None,
        transfer_repo: Optional[BaseRepository[Transfer]] = None,
        session_maker=None,
    ):
        self.account_repo = account_repo or BaseRepository(Account)
        self.transaction_repo = transaction_repo or BaseRepository(Transaction)
        self.transfer_repo = transfer_repo or BaseRepository(Transfer)
        self.session_maker = session_maker or async_session_maker

    async def get_all_accounts(self) -> List[dict[str, Any]]:
        async with self.session_maker() as session:
            accounts = await self.account_repo.get_all(session)
            return [_account_to_dict(account) for account in accounts]

    async def get_account(self, account_id: int) -> dict[str, Any]:
        async with self.session_maker() as session:
            account = await self.account_repo.get(session, account_id)
            return _account_to_dict(account)

    async def get_account_balance(self, account_id: int) -> Decimal:
        async with self.session_maker() as session:
            account = await self.account_repo.get(session, account_id)
            balance = account.opening_balance

            transactions = await self.transaction_repo.get_all(session)
            for transaction in transactions:
                if transaction.account_id == account_id:
                    balance += (
                        transaction.amount
                        if transaction.type == "income"
                        else -transaction.amount
                    )

            transfers = await self.transfer_repo.get_all(session)
            for transfer in transfers:
                if transfer.from_account_id == account_id:
                    balance -= transfer.amount
                if transfer.to_account_id == account_id:
                    balance += transfer.amount

            return balance

    async def add_account(self, account_data: dict[str, Any]) -> dict[str, Any]:
        async with self.session_maker() as session:
            async with session.begin():
                account = Account(
                    name=account_data["name"],
                    opening_balance=account_data.get("opening_balance", 0),
                )
                self._validate_account(account)
                await self._check_existing_accounts(session, account)
                result = await self.account_repo.create(session, account)
            return _account_to_dict(result)

    async def update_account_name(
        self, account_id: int, new_name: str
    ) -> dict[str, Any]:
        async with self.session_maker() as session:
            async with session.begin():
                account = await self.account_repo.get(session, account_id)
                new_account = Account(
                    id=account_id,
                    name=new_name,
                    opening_balance=account.opening_balance,
                )
                self._validate_account(new_account)
                await self._check_existing_accounts(session, new_account)
                updated = await self.account_repo.update(session, new_account)
            return _account_to_dict(updated)

    async def delete_account(self, account_id: int) -> None:
        async with self.session_maker() as session:
            async with session.begin():
                await self.account_repo.delete(session, account_id)

    def _validate_account(self, account: Account):
        if not account.name.strip():
            raise ValueError("Account name cannot be empty")
        if account.opening_balance is None:
            raise ValueError("Account opening balance cannot be empty")

    async def _check_existing_accounts(self, session: AsyncSession, account: Account):
        accounts = await self.account_repo.get_all(session)
        for existing in accounts:
            if existing.name.lower() == account.name.lower() and existing.id != getattr(
                account, "account_id", None
            ):
                raise ValueError("Account name already exists")
