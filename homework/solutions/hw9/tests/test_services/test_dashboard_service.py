from decimal import Decimal

from solution.services.dashboard_service import DashboardService
from unittest.mock import MagicMock


def test_get_dashboard_summary() -> None:
    mock_net_worth = MagicMock()
    mock_report_service = MagicMock()

    mock_net_worth.calculate_net_worth.return_value = Decimal("100")
    mock_report_service.get_monthly_summary.return_value = {
        "total_income": Decimal("100"),
        "total_expense": Decimal("100"),
        "net_cash_flow": Decimal("100"),
    }

    service = DashboardService(mock_net_worth, mock_report_service)
    result = service.get_dashboard_summary()

    assert result == {
        "net_worth": Decimal("100"),
        "total_income": Decimal("100"),
        "total_expense": Decimal("100"),
        "net_cash_flow": Decimal("100"),
    }

    mock_net_worth.calculate_net_worth.assert_called_once()
    mock_report_service.get_monthly_summary.assert_called_once()
