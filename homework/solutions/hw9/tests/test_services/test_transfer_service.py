import pytest
from unittest.mock import MagicMock, AsyncMock
from typing import Any, Dict, List
from solution.services.transfer_service import TransferService
from solution.models.transfer import Transfer


@pytest.fixture
def transfer_service() -> TransferService:
    transfer_repository = MagicMock()
    account_repository = MagicMock()

    session = MagicMock()
    session_maker = MagicMock()
    session_maker.return_value.__aenter__.return_value = session

    service = TransferService(
        transfer_repository=transfer_repository,
        account_repository=account_repository,
        session_maker=session_maker,
    )
    return service


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "transfers_data, output",
    [
        ([], []),
        (
            [
                Transfer(
                    id=1,
                    amount=100,
                    description="Test",
                    from_account_id=1,
                    to_account_id=2,
                    date="2026-03-10",
                )
            ],
            [
                {
                    "id": 1,
                    "amount": 100,
                    "description": "Test",
                    "from_account_id": 1,
                    "to_account_id": 2,
                    "date": "2026-03-10",
                }
            ],
        ),
        (
            [
                Transfer(
                    id=1,
                    amount=100,
                    description="Test2",
                    from_account_id=1,
                    to_account_id=2,
                    date="2026-03-10",
                ),
                Transfer(
                    id=2,
                    amount=50,
                    description="Test2",
                    from_account_id=2,
                    to_account_id=3,
                    date="2026-03-10",
                ),
            ],
            [
                {
                    "id": 1,
                    "amount": 100,
                    "description": "Test2",
                    "from_account_id": 1,
                    "to_account_id": 2,
                    "date": "2026-03-10",
                },
                {
                    "id": 2,
                    "amount": 50,
                    "description": "Test2",
                    "from_account_id": 2,
                    "to_account_id": 3,
                    "date": "2026-03-10",
                },
            ],
        ),
    ],
)
async def test_get_all_transfers(
    transfer_service: TransferService,
    transfers_data: List[Transfer],
    output: List[Dict[str, Any]],
) -> None:
    service = transfer_service
    service.transfer_repository = AsyncMock()
    service.transfer_repository.get_all = AsyncMock(return_value=transfers_data)
    result = await transfer_service.get_all_transfers()
    assert result == output


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "transfer_data, output",
    [
        (
            {
                "amount": 200,
                "description": "Test1",
                "from_account_id": 3,
                "to_account_id": 2,
                "date": "2026-03-10",
            },
            {
                "id": 1,
                "date": "2026-03-10",
                "amount": 200,
                "description": "Test1",
                "from_account_id": 3,
                "to_account_id": 2,
            },
        ),
        (
            {
                "amount": 100,
                "description": "Test",
                "from_account_id": 1,
                "to_account_id": 2,
                "date": "2026-03-10",
            },
            {
                "id": 1,
                "date": "2026-03-10",
                "amount": 100,
                "description": "Test",
                "from_account_id": 1,
                "to_account_id": 2,
            },
        ),
    ],
)
async def test_add_transfer(
    transfer_service: TransferService,
    transfer_data: Dict[str, Any],
    output: Dict[str, Any],
) -> None:

    serviec = transfer_service

    mock_transfer = Transfer(
        id=1,
        amount=transfer_data.get("amount", 0),
        description=transfer_data.get("description", ""),
        from_account_id=transfer_data.get("from_account_id", 0),
        to_account_id=transfer_data.get("to_account_id", 0),
        date="2026-03-10",
    )
    serviec.transfer_repository = AsyncMock()
    serviec.transfer_repository.create = AsyncMock(return_value=mock_transfer)
    serviec.account_repository = AsyncMock()
    serviec.account_repository.get = AsyncMock(return_value=MagicMock())

    result = await serviec.add_transfer(transfer_data)

    assert result == output


@pytest.mark.asyncio
async def test_delete_transfer(transfer_service: TransferService) -> None:
    serviec = transfer_service
    serviec.transfer_repository = AsyncMock()
    serviec.transfer_repository.delete = AsyncMock()
    await serviec.delete_transfer(42)
    serviec.transfer_repository.delete.assert_awaited_once()
