from solution.services.account_service import AccountService
from solution.services.net_worth_service import NetWorth
from solution.services.category_service import CategoryService


from solution.repository.csv_accessor import CsvFileAccessor
from solution.repository.base_repository import BaseRepository

from solution.models.account import Account
from solution.models.transaction import Transaction
from solution.models.transfer import Transfer
from solution.models.categories import Category


# Repositories
account_repository = BaseRepository(
    CsvFileAccessor("data/accounts.csv"),
    Account,
)

transaction_repository = BaseRepository(
    CsvFileAccessor("data/transactions.csv"),
    Transaction,
)

transfer_repository = BaseRepository(
    CsvFileAccessor("data/transfers.csv"),
    Transfer,
)

category_repository = BaseRepository(
    CsvFileAccessor("data/categories.csv"),
    Category,
)


# Service
account_service = AccountService(
    account_repository,
    transaction_repository,
    transfer_repository,
)

net_worth_service = NetWorth(
    account_repository,
    transaction_repository,
    transfer_repository,
)

category_service = CategoryService(
    category_repository
)


def get_account_service() -> AccountService:
    return account_service


def get_net_worth_service() -> NetWorth:
    return net_worth_service


def get_category_service() -> CategoryService:
    return category_service
