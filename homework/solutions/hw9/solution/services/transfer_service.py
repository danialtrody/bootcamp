from solution.repository.base_repository import BaseRepository
from solution.models.transfer import Transfer
from solution.models.account import Account
from typing import Any, Optional, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from solution.database import async_session_maker
import datetime


def _transfer_to_dict(transfer: Transfer) -> dict[str, Any]:
    return {
        "id": transfer.id,
        "amount": transfer.amount,
        "date": transfer.date,
        "description": transfer.description,
        "from_account_id": transfer.from_account_id,
        "to_account_id": transfer.to_account_id,
    }


class TransferService:

    def __init__(
        self,
        transfer_repository: BaseRepository[Transfer],
        account_repository: BaseRepository[Account],
        session_maker: Optional[async_sessionmaker[AsyncSession]] = None,
    ) -> None:
        self.transfer_repository = transfer_repository
        self.account_repository = account_repository
        self.session_maker = session_maker or async_session_maker

    async def get_all_transfers(self) -> List[Dict[str, Any]]:
        async with self.session_maker() as session:
            transfers = await self.transfer_repository.get_all(session)
            return [_transfer_to_dict(transfer) for transfer in transfers]

    async def add_transfer(self, transfer_data: Dict[str, Any]) -> Dict[str, Any]:
        async with self.session_maker() as session:
            async with session.begin():

                transfer = Transfer(
                    amount=transfer_data["amount"],
                    description=transfer_data["description"],
                    from_account_id=transfer_data["from_account_id"],
                    to_account_id=transfer_data["to_account_id"],
                    date=datetime.date.today(),
                )

                if transfer is None:
                    raise ValueError("Transfer cannot be None")

                if transfer.from_account_id == transfer.to_account_id:
                    raise ValueError(
                        "Source and destination accounts must be different"
                    )
                if int(transfer.amount) <= 0:
                    raise ValueError("Transfer amount must be positive")

                await self.account_repository.get(session, transfer.from_account_id)
                await self.account_repository.get(session, transfer.to_account_id)

                created = await self.transfer_repository.create(session, transfer)
            return _transfer_to_dict(created)

    async def delete_transfer(self, transfer_id: int) -> None:
        async with self.session_maker() as session:
            async with session.begin():
                await self.transfer_repository.delete(session, transfer_id)
