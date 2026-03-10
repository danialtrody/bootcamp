from unittest.mock import MagicMock

import pytest
from solution.services.transaction_service import TransactionService
from solution.models.transaction import Transaction
from typing import List
from decimal import Decimal
import datetime
from typing import Optional


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
def test_get_all_transactions_no_filters(test_data: List[Transaction]) -> None:
    mock_repository = MagicMock()
    mock_repository.get_all.return_value = test_data
    service = TransactionService(
        mock_repository,
        account_repository=MagicMock(),
        category_repository=MagicMock()
    )
    result = service.get_all_transactions()

    assert result == test_data
    mock_repository.get_all.assert_called_once()


@pytest.mark.parametrize(
    "test_data, filter,filter_result",
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
def test_get_all_transactions_with_id_filters(
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
    result = service.get_all_transactions(account_id=filter)
    assert result == filter_result
    mock_repository.get_all.assert_called_once()


@pytest.mark.parametrize(
    "test_data, filter,filter_result",
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
def test_get_all_transactions_with_month_filters(
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
    result = service.get_all_transactions(month=filter)
    assert result == filter_result
    mock_repository.get_all.assert_called_once()


@pytest.mark.parametrize(
    "test_data, filter,filter_result",
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
def test_get_all_transactions_with_year_filters(
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
    result = service.get_all_transactions(year=filter)
    assert result == filter_result
    mock_repository.get_all.assert_called_once()


def test_add_income_success() -> None:
    mock_repository = MagicMock()

    transaction = Transaction(
        id=1,
        amount=Decimal("1"),
        date=datetime.date(2025, 3, 3),
        type="",
        account_id=3,
        category_id=3,
    )

    mock_repository.create.return_value = transaction
    service = TransactionService(
        mock_repository,
        account_repository=MagicMock(),
        category_repository=MagicMock()
    )
    result = service.add_income(transaction)

    assert result == transaction
    assert result.type == "income"
    mock_repository.create.assert_called_once_with(transaction)


def test_add_income_fail() -> None:
    mock_repository = MagicMock()

    transaction = Transaction(
        id=1,
        amount=Decimal("-1"),
        date=datetime.date(2025, 3, 3),
        type="",
        account_id=3,
        category_id=3,
    )
    service = TransactionService(
        mock_repository,
        account_repository=MagicMock(),
        category_repository=MagicMock()
    )
    with pytest.raises(ValueError, match="Income amount must be positive"):
        service.add_income(transaction)


def test_add_expense_success() -> None:
    mock_repository = MagicMock()

    transaction = Transaction(
        id=1,
        amount=Decimal("1"),
        date=datetime.date(2025, 3, 3),
        type="",
        account_id=3,
        category_id=3,
    )

    mock_repository.create.return_value = transaction
    service = TransactionService(
        mock_repository,
        account_repository=MagicMock(),
        category_repository=MagicMock()
    )
    result = service.add_expense(transaction)

    assert result == transaction
    assert result.type == "expense"
    mock_repository.create.assert_called_once_with(transaction)


def test_add_expense_fail() -> None:
    mock_repository = MagicMock()

    transaction = Transaction(
        id=1,
        amount=Decimal("-1"),
        date=datetime.date(2025, 3, 3),
        type="",
        account_id=3,
        category_id=3,
    )
    service = TransactionService(
        mock_repository,
        account_repository=MagicMock(),
        category_repository=MagicMock()
    )
    with pytest.raises(ValueError, match="Expense amount must be positive"):
        service.add_expense(transaction)


def test_delete_transactions() -> None:
    mock_repository = MagicMock()
    service = TransactionService(
        mock_repository,
        account_repository=MagicMock(),
        category_repository=MagicMock()
    )
    mock_repository.delete.return_value = None
    service.delete_transaction(1)

    mock_repository.delete.assert_called_once_with(1)
