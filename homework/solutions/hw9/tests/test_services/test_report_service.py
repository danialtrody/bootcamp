from typing import Dict, List, Optional

import pytest
from unittest.mock import MagicMock, AsyncMock
from decimal import Decimal
from datetime import datetime
from solution.services.report_service import ReportService
from solution.models.transaction import Transaction
from solution.models.categories import Category


@pytest.fixture
def report_service() -> ReportService:
    transaction_repository = MagicMock()
    category_repository = MagicMock()

    session = MagicMock()
    session_maker = MagicMock()
    session_maker.return_value.__aenter__.return_value = session

    service = ReportService(
        transaction_repository=transaction_repository,
        category_repository=category_repository,
        session_maker=session_maker,
    )
    return service


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "transactions, month, year, account_id, expected",
    [
        (
            [
                Transaction(
                    id=1,
                    amount=100,
                    type="income",
                    account_id=1,
                    category_id=1,
                    date=datetime(2026, 3, 10),
                ),
                Transaction(
                    id=2,
                    amount=50,
                    type="expense",
                    account_id=1,
                    category_id=2,
                    date=datetime(2026, 3, 15),
                ),
            ],
            3,
            2026,
            None,
            {
                "total_income": Decimal("100"),
                "total_expense": Decimal("50"),
                "net_cash_flow": Decimal("50"),
            },
        ),
        (
            [
                Transaction(
                    id=1,
                    amount=200,
                    type="income",
                    account_id=1,
                    category_id=1,
                    date=datetime(2026, 3, 10),
                ),
            ],
            3,
            2026,
            None,
            {
                "total_income": Decimal("200"),
                "total_expense": Decimal("0"),
                "net_cash_flow": Decimal("200"),
            },
        ),
        (
            [
                Transaction(
                    id=1,
                    amount=200,
                    type="income",
                    account_id=1,
                    category_id=1,
                    date=datetime(2026, 2, 10),
                ),
            ],
            3,
            2026,
            None,
            {
                "total_income": Decimal("0"),
                "total_expense": Decimal("0"),
                "net_cash_flow": Decimal("0"),
            },
        ),
        (
            [
                Transaction(
                    id=1,
                    amount=100,
                    type="income",
                    account_id=1,
                    category_id=1,
                    date=datetime(2026, 3, 10),
                ),
                Transaction(
                    id=2,
                    amount=50,
                    type="income",
                    account_id=2,
                    category_id=1,
                    date=datetime(2026, 3, 10),
                ),
            ],
            3,
            2026,
            1,
            {
                "total_income": Decimal("100"),
                "total_expense": Decimal("0"),
                "net_cash_flow": Decimal("100"),
            },
        ),
    ],
)
async def test_get_monthly_summary(
    report_service: ReportService,
    transactions: List[Transaction],
    month: int,
    year: int,
    account_id: Optional[int],
    expected: Dict[str, Decimal],
) -> None:
    service = report_service
    service.transaction_repository = AsyncMock()
    service.transaction_repository.get_all = AsyncMock(return_value=transactions)

    result = await service.get_monthly_summary(month, year, account_id)
    assert result == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "transactions, categories_data, month, year, account_id, expected",
    [
        (
            [
                Transaction(
                    id=1,
                    amount=100,
                    type="expense",
                    account_id=1,
                    category_id=1,
                    date=datetime(2026, 3, 10),
                ),
                Transaction(
                    id=2,
                    amount=50,
                    type="expense",
                    account_id=1,
                    category_id=2,
                    date=datetime(2026, 3, 15),
                ),
                Transaction(
                    id=3,
                    amount=25,
                    type="income",
                    account_id=1,
                    category_id=1,
                    date=datetime(2026, 3, 20),
                ),
            ],
            [
                Category(id=1, name="Food", type="expense"),
                Category(id=2, name="Rent", type="expense"),
            ],
            3,
            2026,
            None,
            {"Food": Decimal("100"), "Rent": Decimal("50")},
        ),
        (
            [
                Transaction(
                    id=1,
                    amount=30,
                    type="expense",
                    account_id=1,
                    category_id=99,
                    date=datetime(2026, 3, 10),
                ),
            ],
            [],
            3,
            2026,
            None,
            {"Unknown": Decimal("30")},
        ),
    ],
)
async def test_get_spending_breakdown_by_category(
    report_service: ReportService,
    transactions: List[Transaction],
    categories_data: List[Category],
    month: int,
    year: int,
    account_id: Optional[int],
    expected: Dict[str, Decimal],
) -> None:
    service = report_service
    service.transaction_repository = AsyncMock()
    service.category_repository = AsyncMock()
    service.transaction_repository.get_all = AsyncMock(return_value=transactions)
    service.category_repository.get_all = AsyncMock(return_value=categories_data)

    result = await service.get_spending_breakdown_by_category(month, year, account_id)
    assert result == expected
