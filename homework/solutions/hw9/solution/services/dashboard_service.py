from typing import Dict, Any, Optional
import datetime
from solution.services.net_worth_service import NetWorth
from solution.services.report_service import ReportService
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from solution.database import async_session_maker


class DashboardService:

    def __init__(
        self,
        net_worth_service: NetWorth,
        report_service: ReportService,
        session_maker: Optional[async_sessionmaker[AsyncSession]] = None,
    ) -> None:

        self.net_worth_service = net_worth_service
        self.report_service = report_service
        self.session_maker = session_maker or async_session_maker

    async def get_dashboard_summary(self) -> Dict[str, Any]:

        result: Dict[str, Any] = {}
        result["net_worth"] = await self.net_worth_service.calculate_net_worth()

        now = datetime.datetime.now()
        month = now.month
        year = now.year

        get_monthly_summary = await self.report_service.get_monthly_summary(month, year)

        result["total_income"] = get_monthly_summary.get("total_income")
        result["total_expense"] = get_monthly_summary.get("total_expense")
        result["net_cash_flow"] = get_monthly_summary.get("net_cash_flow")

        return result
