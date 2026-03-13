from solution.repository.base_repository import BaseRepository
from solution.models.account import Account
from solution.models.transaction import Transaction
from solution.models.transfer import Transfer
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from solution.database import async_session_maker
from typing import Optional, List


class NetWorth:

    def __init__(
        self,
        account_repository: BaseRepository[Account],
        transaction_repository: BaseRepository[Transaction],
        transfer_repository: BaseRepository[Transfer],
        session_maker: Optional[async_sessionmaker[AsyncSession]] = None,
    ) -> None:
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository
        self.transfer_repository = transfer_repository
        self.session_maker = session_maker or async_session_maker

    async def calculate_net_worth(self) -> Decimal:
        async with self.session_maker() as session:
            net_worth = Decimal("0")

            accounts = await self.account_repository.get_all(session)
            transactions = await self.transaction_repository.get_all(session)

            for account in accounts:
                account_balance = self._calculate_account_balance(account, transactions)
                net_worth += account_balance

            return net_worth

    def _calculate_account_balance(self, account: Account, transactions: List[Transaction]) -> Decimal:
        balance = account.opening_balance
        for transaction in transactions:
            if transaction.account_id != account.id:
                continue
            if transaction.type == "income":
                balance += transaction.amount
            elif transaction.type == "expense":
                balance -= transaction.amount
        return balance
