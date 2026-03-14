import pytest
from unittest.mock import AsyncMock, MagicMock
from decimal import Decimal
from solution.models.account import Account
from solution.models.transaction import Transaction
from solution.services.net_worth_service import NetWorth
from typing import List


@pytest.fixture
def net_worth_service() -> NetWorth:
    account_repository = MagicMock()
    transaction_repository = MagicMock()
    transfer_repository = MagicMock()
    session = MagicMock()
    session_maker = MagicMock()
    session_maker.return_value.__aenter__.return_value = session

    service = NetWorth(
        account_repository=account_repository,
        transaction_repository=transaction_repository,
        transfer_repository=transfer_repository,
        session_maker=session_maker,
    )
    return service


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "accounts, transactions, expected",
    [
        (
            [Account(id=1, name="Account1", opening_balance=100)],
            [
                Transaction(
                    id=1,
                    amount=50,
                    type="income",
                    account_id=1,
                    category_id=1,
                    date="2026-03-10",
                )
            ],
            Decimal("150"),
        ),
        (
            [Account(id=1, name="Account1", opening_balance=200)],
            [
                Transaction(
                    id=1,
                    amount=70,
                    type="expense",
                    account_id=1,
                    category_id=1,
                    date="2026-03-10",
                )
            ],
            Decimal("130"),
        ),
        (
            [Account(id=1, name="Account1", opening_balance=100)],
            [
                Transaction(
                    id=1,
                    amount=50,
                    type="income",
                    account_id=1,
                    category_id=1,
                    date="2026-03-10",
                ),
                Transaction(
                    id=2,
                    amount=30,
                    type="expense",
                    account_id=1,
                    category_id=2,
                    date="2026-03-11",
                ),
            ],
            Decimal("120"),
        ),
        (
            [
                Account(id=1, name="A1", opening_balance=100),
                Account(id=2, name="A2", opening_balance=200),
            ],
            [
                Transaction(
                    id=1,
                    amount=50,
                    type="income",
                    account_id=1,
                    category_id=1,
                    date="2026-03-10",
                ),
                Transaction(
                    id=2,
                    amount=20,
                    type="expense",
                    account_id=2,
                    category_id=2,
                    date="2026-03-11",
                ),
            ],
            Decimal("330"),
        ),
        ([Account(id=1, name="A1", opening_balance=500)], [], Decimal("500")),
    ],
)
async def test_calculate_net_worth_param(
    net_worth_service: NetWorth,
    accounts: List[Account],
    transactions: List[Transaction],
    expected: Decimal,
) -> None:
    service = net_worth_service

    service.account_repository.get_all = AsyncMock(return_value=accounts)
    service.transaction_repository.get_all = AsyncMock(return_value=transactions)

    result = await service.calculate_net_worth()
    assert result == expected
