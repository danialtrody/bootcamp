from typing import Any, Optional, List
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
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
        account_repository: Optional[BaseRepository[Account]] = None,
        transaction_repository: Optional[BaseRepository[Transaction]] = None,
        transfer_repository: Optional[BaseRepository[Transfer]] = None,
        session_maker: Optional[async_sessionmaker[AsyncSession]] = None,
    ):
        self.account_repository = account_repository or BaseRepository(Account)
        self.transaction_repository = transaction_repository or BaseRepository(
            Transaction
        )
        self.transfer_repository = transfer_repository or BaseRepository(Transfer)
        self.session_maker = session_maker or async_session_maker

    async def get_all_accounts(self) -> List[dict[str, Any]]:
        async with self.session_maker() as session:
            accounts = await self.account_repository.get_all(session)
            return [_account_to_dict(account) for account in accounts]

    async def get_account(self, account_id: int) -> dict[str, Any]:
        async with self.session_maker() as session:
            account = await self.account_repository.get(session, account_id)
            return _account_to_dict(account)

    async def get_account_balance(self, account_id: int) -> Decimal:
        async with self.session_maker() as session:
            account = await self.account_repository.get(session, account_id)
            balance = account.opening_balance

            transactions = await self.transaction_repository.get_all(session)
            for transaction in transactions:
                if transaction.account_id == account_id:
                    if transaction.type == "income":
                        balance += transaction.amount
                    else:
                        balance -= transaction.amount

            transfers = await self.transfer_repository.get_all(session)
            for transfer in transfers:
                if transfer.from_account_id == account_id:
                    balance -= transfer.amount
                elif transfer.to_account_id == account_id:
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
                result = await self.account_repository.create(session, account)
            return _account_to_dict(result)

    async def update_account_name(
        self, account_id: int, new_name: str
    ) -> dict[str, Any]:
        async with self.session_maker() as session:
            async with session.begin():
                account = await self.account_repository.get(session, account_id)
                new_account = Account(
                    id=account_id,
                    name=new_name,
                    opening_balance=account.opening_balance,
                )
                self._validate_account(new_account)
                await self._check_existing_accounts(session, new_account)
                updated = await self.account_repository.update(session, new_account)
            return _account_to_dict(updated)

    async def delete_account(self, account_id: int) -> None:
        async with self.session_maker() as session:
            async with session.begin():
                await self.account_repository.delete(session, account_id)

    def _validate_account(self, account: Account) -> None:
        if not account.name.strip():
            raise ValueError("Account name cannot be empty")
        if account.opening_balance is None:
            raise ValueError("Account opening balance cannot be empty")

    async def _check_existing_accounts(self, session: AsyncSession, account: Account) -> None:
        accounts = await self.account_repository.get_all(session)
        for existing in accounts:
            if (
                existing.name.lower() == account.name.lower() and existing.id != account.id
            ):
                raise ValueError("Account name already exists")
