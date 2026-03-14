# flake8: noqa: WPS201

from solution.services.transaction_service import TransactionService
from solution.services.account_service import AccountService
from solution.services.net_worth_service import NetWorth
from solution.services.category_service import CategoryService
from solution.services.transfer_service import TransferService
from solution.services.report_service import ReportService
from solution.services.dashboard_service import DashboardService
# from solution.services.data_portability_service import DataPortabilityService


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

transaction_service = TransactionService(
    transaction_repository,
    account_repository,
    category_repository
)

transfer_service = TransferService(
    transfer_repository,
    account_repository
)

reports_service = ReportService(
    transaction_repository,
    category_repository
)

dashboard_service = DashboardService(
    net_worth_service,
    reports_service
)

# portability_service = DataPortabilityService(
#     account_repository,
#     category_repository,
#     transaction_repository,
#     transfer_repository
# )



def get_account_service() -> AccountService:
    return account_service


def get_net_worth_service() -> NetWorth:
    return net_worth_service


def get_category_service() -> CategoryService:
    return category_service


def get_transaction_service() -> TransactionService:
    return transaction_service


def get_transfer_service() -> TransferService:
    return transfer_service


def get_report_service() -> ReportService:
    return reports_service


def get_dashboard_service() -> DashboardService:
    return dashboard_service

# def get_portability_service() -> DataPortabilityService:
#     return portability_service
