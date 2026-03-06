from solution.repository.base_repository import BaseRepository
from solution.models.transfer import Transfer
from solution.models.account import Account
from typing import List


class TransferService:

    def __init__(
        self,
        transfer_repository: BaseRepository[Transfer],
        account_repository: BaseRepository[Account],
    ) -> None:
        self.transfer_repository = transfer_repository
        self.account_repository = account_repository

    def get_all_transfers(self) -> List[Transfer]:
        return self.transfer_repository.get_all()

    def add_transfer(self, transfer: Transfer) -> Transfer:

        if transfer is None:
            raise ValueError("Transfer cannot be None")

        if transfer.from_account_id == transfer.to_account_id:
            raise ValueError("Source and destination accounts must be different")
        if transfer.amount <= 0:
            raise ValueError("Transfer amount must be positive")

        self.account_repository.get(transfer.from_account_id)
        self.account_repository.get(transfer.to_account_id)

        return self.transfer_repository.create(transfer)

    def delete_transfer(self, transfer_id: int) -> None:
        self.transfer_repository.delete(transfer_id)
