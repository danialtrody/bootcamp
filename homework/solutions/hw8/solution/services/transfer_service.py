from solution.repository.base_repository import BaseRepository
from solution.models.transfer import Transfer
from solution.models.account import Account
from typing import List, Any, Dict
import datetime


class TransferService:

    def __init__(
        self,
        transfer_repository: BaseRepository[Transfer],
        account_repository: BaseRepository[Account],
    ) -> None:
        self.transfer_repository = transfer_repository
        self.account_repository = account_repository

    async def get_all_transfers(self) -> List[Dict[str, Any]]:
        transfers = self.transfer_repository.get_all()
        return [transfer.to_dict() for transfer in transfers]

    async def add_transfer(self, transfer_data: Dict[str, Any]) -> Dict[str, Any]:

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
            raise ValueError("Source and destination accounts must be different")
        if int(transfer.amount) <= 0:
            raise ValueError("Transfer amount must be positive")

        self.account_repository.get(transfer.from_account_id)
        self.account_repository.get(transfer.to_account_id)

        created = self.transfer_repository.create(transfer)
        return created.to_dict()

    async def delete_transfer(self, transfer_id: int) -> None:
        self.transfer_repository.delete(transfer_id)
