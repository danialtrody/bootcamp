from decimal import Decimal
from typing import Any, Dict, List

import pytest
from unittest.mock import MagicMock, AsyncMock
from solution.services.account_service import AccountService
from solution.models.categories import Category
from solution.models.transaction import Transaction


@pytest.fixture
def account_service() -> AccountService:

    account_repository = MagicMock()
    transaction_repository: Transaction = MagicMock()
    transfer_repository = MagicMock()
    Category()

    session = MagicMock()

    session_maker = MagicMock()
    session_maker.return_value.__aenter__.return_value = session

    service = AccountService(
        account_repository=account_repository,
        transaction_repository=transaction_repository,
        transfer_repository=transfer_repository,
        session_maker=session_maker,
    )

    return service


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "accounts_data, expected",
    [
        ([], []),
        ([(1, "Cash", 100)], [{"id": 1, "name": "Cash", "opening_balance": 100}]),
        (
            [(1, "TEST1", 1), (2, "TEST2", 2), (3, "TEST3", 3)],
            [
                {"id": 1, "name": "TEST1", "opening_balance": 1},
                {"id": 2, "name": "TEST2", "opening_balance": 2},
                {"id": 3, "name": "TEST3", "opening_balance": 3},
            ],
        ),
    ],
)
async def test_get_all_accounts(
    account_service: AccountService,
    accounts_data: List[tuple],
    expected: List[Dict[str, Any]],
) -> None:
    service = account_service

    test_accounts = []
    for id, name, opening_balance in accounts_data:
        account = MagicMock()
        account.id = id
        account.name = name
        account.opening_balance = opening_balance
        test_accounts.append(account)
    service.account_repository = AsyncMock()
    service.account_repository.get_all = AsyncMock(return_value=test_accounts)
    result = await service.get_all_accounts()
    assert result == expected


@pytest.mark.asyncio
async def test_get_account(account_service: AccountService) -> None:
    service = account_service

    test_accont = MagicMock()
    test_accont.id = 1
    test_accont.name = "Cash"
    test_accont.opening_balance = 100

    service.account_repository = AsyncMock()
    service.account_repository.get = AsyncMock()
    service.account_repository.get.return_value = test_accont

    result = await service.get_account(test_accont.id)

    assert result == {"id": 1, "name": "Cash", "opening_balance": 100}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "account_id, test_account, test_transaction, test_transfer, output",
    [
        (
            1,
            MagicMock(id=1, name="cash", opening_balance=100),
            [
                MagicMock(
                    id=1,
                    amount=100,
                    date="2026-03-10",
                    type="income",
                    account_id=1,
                    category_id=1,
                ),
                MagicMock(
                    id=2,
                    amount=100,
                    date="2026-03-10",
                    type="income",
                    account_id=1,
                    category_id=1,
                ),
                MagicMock(
                    id=3,
                    amount=50,
                    date="2026-03-10",
                    type="expense",
                    account_id=1,
                    category_id=1,
                ),
            ],
            [
                MagicMock(
                    id=1,
                    amount=10,
                    date="2026-03-10",
                    description="",
                    from_account_id=2,
                    to_account_id=1,
                ),
                MagicMock(
                    id=1,
                    amount=10,
                    date="2026-03-10",
                    description="",
                    from_account_id=1,
                    to_account_id=2,
                ),
            ],
            250,
        ),
    ],
)
async def testget_account_balance(
    account_service: AccountService,
    account_id: int,
    test_account: List[MagicMock],
    test_transaction: List[MagicMock],
    test_transfer: List[MagicMock],
    output: Decimal,
) -> None:
    service = account_service
    service.transaction_repository

    service.account_repository = AsyncMock()
    service.account_repository.get = AsyncMock()
    service.account_repository.get.return_value = test_account

    service.transaction_repository = AsyncMock()
    service.transaction_repository.get_all.return_value = test_transaction

    service.transfer_repository = AsyncMock()
    service.transfer_repository.get_all.return_value = test_transfer

    result = await service.get_account_balance(account_id)
    assert result == output


@pytest.mark.asyncio
async def test_add_account(account_service: AccountService) -> None:
    service = account_service

    mock_account = MagicMock()
    mock_account.id = 1
    mock_account.name = "TEST"
    mock_account.opening_balance = 100

    service.account_repository = AsyncMock()
    service.account_repository.create = AsyncMock()
    service.account_repository.get_all = AsyncMock(return_value=[])
    service.account_repository.create.return_value = mock_account
    result = await service.add_account(mock_account)

    assert result == {"id": 1, "name": "TEST", "opening_balance": 100}


@pytest.mark.asyncio
async def test_update_account_name(account_service: AccountService) -> None:
    service = account_service

    mock_account = MagicMock()
    mock_account.id = 1
    mock_account.name = "TEST"
    mock_account.opening_balance = 0

    service.account_repository = AsyncMock()
    service.account_repository.get = AsyncMock(return_value=mock_account)
    service.account_repository.get_all = AsyncMock(return_value=[mock_account])
    mock_account.name = "updated_name"
    service.account_repository.update = AsyncMock(return_value=mock_account)

    result = await service.update_account_name(1, "updated_name")

    assert result == {"id": 1, "name": "updated_name", "opening_balance": 0}


@pytest.mark.asyncio
async def test_delete_account(account_service: AccountService) -> None:
    service = account_service
    service.account_repository = AsyncMock()
    service.account_repository.delete = AsyncMock()
    await service.delete_account(42)
    service.account_repository.delete.assert_awaited_once()
