import zipfile
import os
import csv
from decimal import Decimal
from datetime import datetime
from typing import List, Dict, Set
from solution.models.account import Account
from solution.models.categories import Category, CategoryType
from solution.models.transaction import Transaction
from solution.models.transfer import Transfer
from solution.repository.base_repository import BaseRepository


EXPORT_ZIP_FILE_NAME = "data.zip"
DATA_FOLDER = "data"
TEMP_FOLDER = "temp_import"

ACCOUNTS_FILE = "accounts.csv"
CATEGORIES_FILE = "categories.csv"
TRANSACTIONS_FILE = "transactions.csv"
TRANSFERS_FILE = "transfers.csv"

ID_FIELD = "id"


class DataPortabilityService:

    def __init__(
        self,
        account_repository: BaseRepository[Account],
        category_repository: BaseRepository[Category],
        transaction_repository: BaseRepository[Transaction],
        transfer_repository: BaseRepository[Transfer],
    ) -> None:

        self.account_repository = account_repository
        self.category_repository = category_repository
        self.transaction_repository = transaction_repository
        self.transfer_repository = transfer_repository

    def export(self) -> str:

        os.makedirs(DATA_FOLDER, exist_ok=True)
        with zipfile.ZipFile(
            EXPORT_ZIP_FILE_NAME,
            "w",
        ) as zip_file:
            files = [
                ACCOUNTS_FILE,
                CATEGORIES_FILE,
                TRANSACTIONS_FILE,
                TRANSFERS_FILE,
            ]

            for file_name in files:
                file_path = os.path.join(DATA_FOLDER, file_name)

                if not os.path.exists(file_path):
                    raise ValueError(f"Missing file: {file_name}")

                zip_file.write(file_path, file_name)

        return EXPORT_ZIP_FILE_NAME

    def import_from_zip(self, zip_path: str) -> None:

        if not os.path.exists(zip_path):
            raise ValueError("Zip file does not exist")

        os.makedirs(TEMP_FOLDER, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zip_file:
            zip_file.extractall(TEMP_FOLDER)

        self.validate_import_files(TEMP_FOLDER)
        self.validate_referential_integrity(TEMP_FOLDER)

        self.clear_database()

        self.import_accounts(TEMP_FOLDER)
        self.import_categories(TEMP_FOLDER)
        self.import_transactions(TEMP_FOLDER)
        self.import_transfers(TEMP_FOLDER)

    def validate_import_files(self, path: str) -> None:

        required_files = [
            ACCOUNTS_FILE,
            CATEGORIES_FILE,
            TRANSACTIONS_FILE,
            TRANSFERS_FILE,
        ]

        for file_name in required_files:

            file_path = os.path.join(path, file_name)

            if not os.path.exists(file_path):
                raise ValueError(f"Missing required file: {file_name}")

            with open(file_path, "r") as file:
                reader = csv.DictReader(file)

                if reader.fieldnames is None:
                    raise ValueError(f"Invalid CSV structure: {file_name}")

    def clear_database(self) -> None:

        for transaction in self.transaction_repository.get_all():
            self.transaction_repository.delete(transaction.id)

        for transfer in self.transfer_repository.get_all():
            self.transfer_repository.delete(transfer.id)

        for category in self.category_repository.get_all():
            self.category_repository.delete(category.id)

        for account in self.account_repository.get_all():
            self.account_repository.delete(account.id)

    def load_csv(self, file_path: str) -> List[Dict[str, str]]:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            return list(reader)

    def import_accounts(self, path: str) -> None:

        data = self.load_csv(os.path.join(path, "accounts.csv"))

        for row in data:
            account = Account(
                id=int(row[ID_FIELD]),
                name=row["name"],
                opening_balance=Decimal(row["opening_balance"]),
            )
            self.account_repository.create(account)

    def import_categories(self, path: str) -> None:

        data = self.load_csv(os.path.join(path, "categories.csv"))
        for row in data:
            category = Category(
                id=int(row[ID_FIELD]),
                name=row["name"],
                type=CategoryType(row["type"]),
            )
            self.category_repository.create(category)

    def import_transactions(self, path: str) -> None:

        data = self.load_csv(os.path.join(path, "transactions.csv"))
        for row in data:
            transaction = Transaction(
                id=int(row[ID_FIELD]),
                amount=Decimal(row["amount"]),
                date=datetime.strptime(row["date"], "%Y-%m-%d").date(),
                type=row["type"],
                account_id=int(row["account_id"]),
                category_id=int(row["category_id"]),
            )
            self.transaction_repository.create(transaction)

    def import_transfers(self, path: str) -> None:

        data = self.load_csv(os.path.join(path, "transfers.csv"))
        for row in data:
            transfer = Transfer(
                id=int(row[ID_FIELD]),
                amount=Decimal(row["amount"]),
                date=datetime.strptime(row["date"], "%Y-%m-%d").date(),
                description=row.get("description", ""),
                from_account_id=int(row["from_account_id"]),
                to_account_id=int(row["to_account_id"]),
            )
            self.transfer_repository.create(transfer)

    def validate_referential_integrity(self, path: str) -> None:

        accounts = self.load_csv(os.path.join(path, ACCOUNTS_FILE))
        categories = self.load_csv(os.path.join(path, CATEGORIES_FILE))
        transactions = self.load_csv(os.path.join(path, TRANSACTIONS_FILE))
        transfers = self.load_csv(os.path.join(path, TRANSFERS_FILE))

        accounts_ids = {int(account[ID_FIELD]) for account in accounts}
        categories_ids = {int(category[ID_FIELD]) for category in categories}

        self._validate_transactions(transactions, accounts_ids, categories_ids)
        self._validate_transfers(transfers, accounts_ids)

    def _validate_transactions(
        self,
        transactions: List[Dict[str, str]],
        accounts_ids: Set[int],
        categories_ids: Set[int],
    ) -> None:

        for transaction in transactions:
            if int(transaction["account_id"]) not in accounts_ids:
                raise ValueError(
                    f"Invalid account reference in transaction {transaction[ID_FIELD]}"
                )
            if int(transaction["category_id"]) not in categories_ids:
                raise ValueError(
                    f"Invalid category reference in transaction {transaction[ID_FIELD]}"
                )

    def _validate_transfers(
        self,
        transfers: List[Dict[str, str]],
        accounts_ids: Set[int],
    ) -> None:

        for transfer in transfers:

            from_id = int(transfer["from_account_id"])
            to_id = int(transfer["to_account_id"])

            if from_id not in accounts_ids:
                raise ValueError(
                    f"Invalid source account in transfer {transfer[ID_FIELD]}"
                )

            if to_id not in accounts_ids:
                raise ValueError(
                    f"Invalid destination account in transfer {transfer[ID_FIELD]}"
                )

            if from_id == to_id:
                raise ValueError(
                    f"Transfer {transfer[ID_FIELD]} has same source and destination"
                )
