from decimal import Decimal
from typing import Dict
import pytest
from unittest.mock import MagicMock, AsyncMock
from solution.services.dashboard_service import DashboardService


@pytest.fixture
def dashboard_service() -> DashboardService:

    net_worth_service = MagicMock()
    report_service = MagicMock()

    session = MagicMock()
    session_maker = MagicMock()
    session_maker.return_value.__aenter__.return_value = session

    service = DashboardService(
        net_worth_service=net_worth_service,
        report_service=report_service,
        session_maker=session_maker,
    )

    return service


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "monthly_summary, net_worth_value, expected",
    [
        (
            {"total_income": 100, "total_expense": 20, "net_cash_flow": 80},
            Decimal("1000"),
            {
                "total_income": 100,
                "total_expense": 20,
                "net_cash_flow": 80,
                "net_worth": 1000,
            },
        ),
        (
            {"total_income": 200, "total_expense": 50, "net_cash_flow": 150},
            Decimal("2500"),
            {
                "total_income": 200,
                "total_expense": 50,
                "net_cash_flow": 150,
                "net_worth": 2500,
            },
        ),
        (
            {"total_income": 0, "total_expense": 0, "net_cash_flow": 0},
            Decimal("0"),
            {"total_income": 0, "total_expense": 0, "net_cash_flow": 0, "net_worth": 0},
        ),
    ],
)
async def test_get_dashboard_summary_param(
    dashboard_service: DashboardService,
    monthly_summary: Dict,
    net_worth_value: Decimal,
    expected: Dict,
) -> None:
    service = dashboard_service
    service.net_worth_service = AsyncMock()
    service.net_worth_service.calculate_net_worth = AsyncMock(
        return_value=net_worth_value
    )
    service.report_service = AsyncMock()
    service.report_service.get_monthly_summary = AsyncMock(return_value=monthly_summary)

    result = await service.get_dashboard_summary()

    assert result == expected
