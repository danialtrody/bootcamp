from unittest.mock import MagicMock
from solution.services.report_service import ReportService
from solution.models.transaction import Transaction
from solution.models.categories import Category, CategoryType

import datetime
from decimal import Decimal


def test_get_monthly_summary_single_account() -> None:
    mock_transaction = MagicMock()
    mock_category = MagicMock()

    mock_transaction.get_all.return_value = [
        Transaction(
            id=1,
            amount=Decimal("50"),
            date=datetime.date(2026, 1, 1),
            type="income",
            account_id=1,
            category_id=1,
        )
    ]

    service = ReportService(mock_transaction, mock_category)
    result = service.get_monthly_summary(1, 2026, 1)

    expected = {
        "total_income": Decimal("50"),
        "total_expense": Decimal("0"),
        "net_cash_flow": Decimal("50"),
    }

    assert result == expected


def test_get_monthly_summary_multiple_accounts() -> None:
    mock_transaction = MagicMock()
    mock_category = MagicMock()

    mock_transaction.get_all.return_value = [
        Transaction(
            id=1,
            amount=Decimal("50"),
            date=datetime.date(2026, 1, 1),
            type="income",
            account_id=1,
            category_id=1,
        ),
        Transaction(
            id=1,
            amount=Decimal("20"),
            date=datetime.date(2026, 1, 1),
            type="expense",
            account_id=1,
            category_id=1,
        ),
        Transaction(
            id=1,
            amount=Decimal("30"),
            date=datetime.date(2026, 1, 1),
            type="income",
            account_id=1,
            category_id=1,
        ),
    ]

    service = ReportService(mock_transaction, mock_category)
    result = service.get_monthly_summary(1, 2026, 1)

    expected = {
        "total_income": Decimal("80"),
        "total_expense": Decimal("20"),
        "net_cash_flow": Decimal("60"),
    }

    assert result == expected


def test_get_monthly_summary_zero_accounts() -> None:
    mock_transaction = MagicMock()
    mock_category = MagicMock()
    mock_transaction.get_all.return_value = []
    service = ReportService(mock_transaction, mock_category)
    result = service.get_monthly_summary(1, 2026, 1)

    expected = {
        "total_income": Decimal("0"),
        "total_expense": Decimal("0"),
        "net_cash_flow": Decimal("0"),
    }

    assert result == expected


def test_get_spending_breakdown_by_category() -> None:
    mock_transaction = MagicMock()
    mock_category = MagicMock()

    mock_category.get_all.return_value = [
        Category(id=1, name="TEST1", type=CategoryType.INCOME),
        Category(id=2, name="TEST2", type=CategoryType.INCOME),
        Category(id=3, name="TEST3", type=CategoryType.EXPENSE),
    ]

    mock_transaction.get_all.return_value = [
        Transaction(
            id=1,
            amount=Decimal("50"),
            date=datetime.date(2026, 1, 1),
            type="expense",
            account_id=1,
            category_id=1,
        ),
        Transaction(
            id=2,
            amount=Decimal("60"),
            date=datetime.date(2026, 1, 1),
            type="expense",
            account_id=1,
            category_id=2,
        ),
        Transaction(
            id=3,
            amount=Decimal("60"),
            date=datetime.date(2026, 1, 1),
            type="expense",
            account_id=1,
            category_id=2,
        ),
    ]

    service = ReportService(mock_transaction, mock_category)
    result = service.get_spending_breakdown_by_category(1, 2026, 1)

    assert result == {"TEST1": Decimal("50"), "TEST2": Decimal("120")}
