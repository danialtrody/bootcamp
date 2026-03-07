from solution.services.account_service import AccountService
from solution.services.net_worth_service import NetWorth


from solution.repository.csv_accessor import CsvFileAccessor
from solution.repository.base_repository import BaseRepository

from solution.models.account import Account
from solution.models.transaction import Transaction
from solution.models.transfer import Transfer

# Repositories
account_repo = BaseRepository(
    CsvFileAccessor("data/accounts.csv"),
    Account,
)

transaction_repo = BaseRepository(
    CsvFileAccessor("data/transactions.csv"),
    Transaction,
)

transfer_repo = BaseRepository(
    CsvFileAccessor("data/transfers.csv"),
    Transfer,
)


# Service
account_service = AccountService(
    account_repo,
    transaction_repo,
    transfer_repo,
)

net_worth_service = NetWorth(
    account_repo,
    transaction_repo,
    transfer_repo,
)


def get_account_service() -> AccountService:
    return account_service


def get_net_worth_service() -> NetWorth:
    return net_worth_service
