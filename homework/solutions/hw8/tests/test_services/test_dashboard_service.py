from decimal import Decimal
import pytest
from unittest.mock import AsyncMock
from solution.services.dashboard_service import DashboardService


@pytest.mark.asyncio
async def test_get_dashboard_summary() -> None:
    mock_net_worth = AsyncMock()
    mock_report_service = AsyncMock()

    mock_net_worth.calculate_net_worth.return_value = Decimal("100")
    mock_report_service.get_monthly_summary.return_value = {
        "total_income": Decimal("100"),
        "total_expense": Decimal("100"),
        "net_cash_flow": Decimal("100"),
    }

    service = DashboardService(mock_net_worth, mock_report_service)
    result = await service.get_dashboard_summary()

    assert result["net_worth"] == Decimal("100")
    assert result["total_income"] == Decimal("100")
    assert result["total_expense"] == Decimal("100")
    assert result["net_cash_flow"] == Decimal("100")

    mock_net_worth.calculate_net_worth.assert_awaited_once()
    mock_report_service.get_monthly_summary.assert_awaited_once()
