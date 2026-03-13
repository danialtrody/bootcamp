from unittest.mock import MagicMock
import pytest
from solution.services.transaction_service import TransactionService
from solution.models.transaction import Transaction
from typing import List, Optional
from decimal import Decimal
import datetime


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_data",
    [
        (
            [
                Transaction(
                    id=1,
                    amount=Decimal("0"),
                    date=datetime.date(2026, 1, 1),
                    type="income",
                    account_id=1,
                    category_id=1,
                )
            ]
        ),
        (
            [
                Transaction(
                    id=1,
                    amount=Decimal("100"),
                    date=datetime.date(2026, 1, 1),
                    type="income",
                    account_id=1,
                    category_id=1,
                ),
                Transaction(
                    id=2,
                    amount=Decimal("1"),
                    date=datetime.date(2026, 1, 2),
                    type="expense",
                    account_id=2,
                    category_id=2,
                ),
            ]
        ),
    ],
)
async def test_get_all_transactions_no_filters(test_data: List[Transaction]) -> None:
    mock_repository = MagicMock()
    mock_repository.get_all.return_value = test_data
    service = TransactionService(
        mock_repository,
        account_repository=MagicMock(),
        category_repository=MagicMock()
    )
    result = await service.get_all_transactions()

    expected = [transaction.to_dict() for transaction in test_data]
    assert result == expected
    mock_repository.get_all.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_data, filter, filter_result",
    [
        (
            [
                Transaction(
                    id=1,
                    amount=Decimal("100"),
                    date=datetime.date(2026, 1, 1),
                    type="income",
                    account_id=1,
                    category_id=1,
                ),
                Transaction(
                    id=2,
                    amount=Decimal("1"),
                    date=datetime.date(2026, 1, 1),
                    type="expense",
                    account_id=2,
                    category_id=2,
                ),
                Transaction(
                    id=3,
                    amount=Decimal("1"),
                    date=datetime.date(2025, 3, 3),
                    type="expense",
                    account_id=3,
                    category_id=3,
                ),
            ],
            1,
            [
                Transaction(
                    id=1,
                    amount=Decimal("100"),
                    date=datetime.date(2026, 1, 1),
                    type="income",
                    account_id=1,
                    category_id=1,
                )
            ],
        ),
    ],
)
async def test_get_all_transactions_with_id_filters(
    test_data: List[Transaction],
    filter: int,
    filter_result: List[Transaction],
) -> None:
    mock_repository = MagicMock()
    mock_repository.get_all.return_value = test_data
    service = TransactionService(
        mock_repository,
        account_repository=MagicMock(),
        category_repository=MagicMock()
    )
    result = await service.get_all_transactions(account_id=filter)
    expected = [transaction.to_dict() for transaction in filter_result]
    assert result == expected
    mock_repository.get_all.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_data, filter, filter_result",
    [
        (
            [
                Transaction(
                    id=1,
                    amount=Decimal("100"),
                    date=datetime.date(2026, 1, 1),
                    type="income",
                    account_id=1,
                    category_id=1,
                ),
                Transaction(
                    id=2,
                    amount=Decimal("1"),
                    date=datetime.date(2026, 2, 2),
                    type="expense",
                    account_id=2,
                    category_id=2,
                ),
                Transaction(
                    id=3,
                    amount=Decimal("1"),
                    date=datetime.date(2025, 3, 3),
                    type="expense",
                    account_id=3,
                    category_id=3,
                ),
            ],
            1,
            [
                Transaction(
                    id=1,
                    amount=Decimal("100"),
                    date=datetime.date(2026, 1, 1),
                    type="income",
                    account_id=1,
                    category_id=1,
                )
            ],
        ),
    ],
)
async def test_get_all_transactions_with_month_filters(
    test_data: List[Transaction],
    filter: Optional[int],
    filter_result: List[Transaction],
) -> None:
    mock_repository = MagicMock()
    mock_repository.get_all.return_value = test_data
    service = TransactionService(
        mock_repository,
        account_repository=MagicMock(),
        category_repository=MagicMock()
    )
    result = await service.get_all_transactions(month=filter)
    expected = [transaction.to_dict() for transaction in filter_result]
    assert result == expected
    mock_repository.get_all.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_data, filter, filter_result",
    [
        (
            [
                Transaction(
                    id=1,
                    amount=Decimal("100"),
                    date=datetime.date(2026, 1, 1),
                    type="income",
                    account_id=1,
                    category_id=1,
                ),
                Transaction(
                    id=2,
                    amount=Decimal("1"),
                    date=datetime.date(2026, 2, 2),
                    type="expense",
                    account_id=2,
                    category_id=2,
                ),
                Transaction(
                    id=3,
                    amount=Decimal("1"),
                    date=datetime.date(2025, 3, 3),
                    type="expense",
                    account_id=3,
                    category_id=3,
                ),
            ],
            2025,
            [
                Transaction(
                    id=3,
                    amount=Decimal("1"),
                    date=datetime.date(2025, 3, 3),
                    type="expense",
                    account_id=3,
                    category_id=3,
                )
            ],
        ),
    ],
)
async def test_get_all_transactions_with_year_filters(
    test_data: List[Transaction],
    filter: Optional[int],
    filter_result: List[Transaction],
) -> None:
    mock_repository = MagicMock()
    mock_repository.get_all.return_value = test_data
    service = TransactionService(
        mock_repository,
        account_repository=MagicMock(),
        category_repository=MagicMock()
    )
    result = await service.get_all_transactions(year=filter)
    expected = [transaction.to_dict() for transaction in filter_result]
    assert result == expected
    mock_repository.get_all.assert_called_once()


@pytest.mark.asyncio
async def test_add_income_success() -> None:
    mock_repository = MagicMock()
    transaction_data = {
        "amount": Decimal("1"),
        "date": datetime.date(2025, 3, 3),
        "account_id": 3,
        "category_id": 3,
    }
    created_transaction = Transaction(
        id=1,
        amount=Decimal("1"),
        date=datetime.date(2025, 3, 3),
        type="income",
        account_id=3,
        category_id=3,
    )
    mock_repository.create.return_value = created_transaction

    service = TransactionService(
        mock_repository,
        account_repository=MagicMock(exists=MagicMock(return_value=True)),
        category_repository=MagicMock(exists=MagicMock(return_value=True))
    )
    result = await service.add_income(transaction_data)

    assert result == created_transaction.to_dict()
    assert result["type"] == "income"
    mock_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_add_income_fail() -> None:
    mock_repository = MagicMock()
    transaction_data = {
        "amount": Decimal("-1"),
        "date": datetime.date(2025, 3, 3),
        "account_id": 3,
        "category_id": 3,
    }
    service = TransactionService(
        mock_repository,
        account_repository=MagicMock(exists=MagicMock(return_value=True)),
        category_repository=MagicMock(exists=MagicMock(return_value=True))
    )
    with pytest.raises(ValueError, match="Income amount must be positive"):
        await service.add_income(transaction_data)


@pytest.mark.asyncio
async def test_add_expense_success() -> None:
    mock_repository = MagicMock()
    transaction_data = {
        "amount": Decimal("1"),
        "date": datetime.date(2025, 3, 3),
        "account_id": 3,
        "category_id": 3,
    }
    created_transaction = Transaction(
        id=1,
        amount=Decimal("1"),
        date=datetime.date(2025, 3, 3),
        type="expense",
        account_id=3,
        category_id=3,
    )
    mock_repository.create.return_value = created_transaction

    service = TransactionService(
        mock_repository,
        account_repository=MagicMock(exists=MagicMock(return_value=True)),
        category_repository=MagicMock(exists=MagicMock(return_value=True))
    )
    result = await service.add_expense(transaction_data)

    assert result == created_transaction.to_dict()
    assert result["type"] == "expense"
    mock_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_add_expense_fail() -> None:
    mock_repository = MagicMock()
    transaction_data = {
        "amount": Decimal("-1"),
        "date": datetime.date(2025, 3, 3),
        "account_id": 3,
        "category_id": 3,
    }
    service = TransactionService(
        mock_repository,
        account_repository=MagicMock(exists=MagicMock(return_value=True)),
        category_repository=MagicMock(exists=MagicMock(return_value=True))
    )
    with pytest.raises(ValueError, match="Expense amount must be positive"):
        await service.add_expense(transaction_data)


@pytest.mark.asyncio
async def test_delete_transactions() -> None:
    mock_repository = MagicMock()
    service = TransactionService(
        mock_repository,
        account_repository=MagicMock(),
        category_repository=MagicMock()
    )
    mock_repository.delete.return_value = None
    await service.delete_transaction(1)

    mock_repository.delete.assert_called_once_with(1)
