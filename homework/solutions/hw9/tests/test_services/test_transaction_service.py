import pytest
from unittest.mock import MagicMock, AsyncMock
from decimal import Decimal
from datetime import date
from typing import List, Dict, Any, Optional
from solution.services.transaction_service import TransactionService
from solution.models.transaction import Transaction


@pytest.fixture
def transaction_service() -> TransactionService:
    transaction_repository = MagicMock()
    account_repository = MagicMock()
    category_repository = MagicMock()

    session = MagicMock()
    session_maker = MagicMock()
    session_maker.return_value.__aenter__.return_value = session

    service = TransactionService(
        transaction_repository=transaction_repository,
        account_repository=account_repository,
        category_repository=category_repository,
        session_maker=session_maker,
    )
    return service


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "transactions, account_id, month, year, expected",
    [
        (
            [
                Transaction(
                    id=1,
                    amount=Decimal("100"),
                    type="income",
                    account_id=1,
                    category_id=1,
                    date=date(2026, 3, 10),
                ),
                Transaction(
                    id=2,
                    amount=Decimal("50"),
                    type="expense",
                    account_id=1,
                    category_id=2,
                    date=date(2026, 3, 15),
                ),
            ],
            None,
            None,
            None,
            [
                {
                    "id": 1,
                    "amount": 100.0,
                    "type": "income",
                    "account_id": 1,
                    "category_id": 1,
                    "date": date(2026, 3, 10),
                },
                {
                    "id": 2,
                    "amount": 50.0,
                    "type": "expense",
                    "account_id": 1,
                    "category_id": 2,
                    "date": date(2026, 3, 15),
                },
            ],
        ),
        (
            [
                Transaction(
                    id=1,
                    amount=Decimal("100"),
                    type="income",
                    account_id=1,
                    category_id=1,
                    date=date(2026, 3, 10),
                ),
                Transaction(
                    id=2,
                    amount=Decimal("50"),
                    type="expense",
                    account_id=2,
                    category_id=2,
                    date=date(2026, 3, 15),
                ),
            ],
            1,
            3,
            2026,
            [
                {
                    "id": 1,
                    "amount": 100.0,
                    "type": "income",
                    "account_id": 1,
                    "category_id": 1,
                    "date": date(2026, 3, 10),
                },
            ],
        ),
    ],
)
async def test_get_all_transactions(
    transaction_service: TransactionService,
    transactions: List[Transaction],
    account_id: Optional[int],
    month: Optional[int],
    year: Optional[int],
    expected: List[Dict[str, Any]],
) -> None:
    service = transaction_service
    service.transaction_repository = AsyncMock()
    service.transaction_repository.get_all = AsyncMock(return_value=transactions)

    result = await transaction_service.get_all_transactions(account_id, month, year)
    assert result == expected


@pytest.mark.asyncio
async def test_add_income(transaction_service: TransactionService) -> None:
    service = transaction_service

    transaction_data = {
        "amount": Decimal("100"),
        "account_id": 1,
        "category_id": 1,
    }

    mock_transaction = Transaction(
        id=1,
        amount=Decimal("100"),
        type="income",
        account_id=1,
        category_id=1,
        date="2026-03-10",
    )
    service.account_repository = AsyncMock()
    service.category_repository = AsyncMock()
    service.transaction_repository = AsyncMock()
    service.account_repository.exists = AsyncMock(return_value=True)
    service.category_repository.exists = AsyncMock(return_value=True)
    service.transaction_repository.create = AsyncMock(return_value=mock_transaction)

    result = await service.add_income(transaction_data)

    assert result == {
        "id": 1,
        "amount": 100,
        "account_id": 1,
        "category_id": 1,
        "date": "2026-03-10",
        "type": "income",
    }


@pytest.mark.asyncio
async def test_add_expense(transaction_service: TransactionService) -> None:
    service = transaction_service

    transaction_data = {
        "amount": Decimal("100"),
        "account_id": 1,
        "category_id": 3,
    }

    mock_transaction = Transaction(
        id=1,
        amount=Decimal("100"),
        type="expense",
        account_id=1,
        category_id=3,
        date="2026-03-10",
    )

    service.account_repository = AsyncMock()
    service.category_repository = AsyncMock()
    service.transaction_repository = AsyncMock()
    service.account_repository.exists = AsyncMock(return_value=True)
    service.category_repository.exists = AsyncMock(return_value=True)
    service.transaction_repository.create = AsyncMock(return_value=mock_transaction)

    result = await service.add_expense(transaction_data)

    assert result == {
        "id": 1,
        "amount": 100,
        "account_id": 1,
        "category_id": 3,
        "date": "2026-03-10",
        "type": "expense",
    }


@pytest.mark.asyncio
async def test_delete_transaction(transaction_service: TransactionService) -> None:
    service = transaction_service
    service.transaction_repository = AsyncMock()
    service.transaction_repository.delete = AsyncMock()
    await service.delete_transaction(50)
    service.transaction_repository.delete.assert_awaited_once()
