from unittest.mock import MagicMock

import pytest
from solution.services.transfer_service import TransferService
from solution.models.transfer import Transfer
from typing import List
from decimal import Decimal
import datetime


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "transfer",
    [
        [
            Transfer(
                id=1,
                amount=Decimal("0"),
                date=datetime.date(2026, 1, 1),
                description="TEST",
                from_account_id=1,
                to_account_id=2,
            )
        ],
        [
            Transfer(
                id=1,
                amount=Decimal("100"),
                date=datetime.date(2026, 1, 1),
                description="TEST",
                from_account_id=1,
                to_account_id=2,
            ),
            Transfer(
                id=2,
                amount=Decimal("1"),
                date=datetime.date(2026, 1, 2),
                description="TEST2",
                from_account_id=3,
                to_account_id=4,
            ),
        ],
    ],
)
async def test_get_all_transfers(transfer: List[Transfer]) -> None:
    mock_transfer_repo = MagicMock()
    mock_account_repo = MagicMock()
    mock_transfer_repo.get_all.return_value = transfer
    service = TransferService(mock_transfer_repo, mock_account_repo)
    result = await service.get_all_transfers()

    expected = [transfer.to_dict() for transfer in transfer]

    assert result == expected
    mock_transfer_repo.get_all.assert_called_once()


@pytest.mark.asyncio
async def test_add_transfer_success() -> None:
    mock_transfer_repo = MagicMock()
    mock_account_repo = MagicMock()

    transfer = Transfer(
        id=1,
        amount=Decimal("100"),
        date=datetime.date(2026, 1, 1),
        description="TEST",
        from_account_id=1,
        to_account_id=2,
    )

    service = TransferService(mock_transfer_repo, mock_account_repo)

    mock_transfer_repo.create.return_value = transfer

    result = await service.add_transfer(transfer.to_dict())

    assert result == transfer.to_dict()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "transfer, error",
    [
        (
            Transfer(
                id=1,
                amount=Decimal("100"),
                date=datetime.date(2026, 1, 1),
                description="TEST",
                from_account_id=1,
                to_account_id=1,
            ),
            "Source and destination accounts must be different",
        ),
        (
            Transfer(
                id=1,
                amount=Decimal("-1"),
                date=datetime.date(2026, 1, 1),
                description="TEST",
                from_account_id=1,
                to_account_id=2,
            ),
            "Transfer amount must be positive",
        ),
    ],
)
async def test_add_transfer_fail(transfer: Transfer, error: str) -> None:
    mock_transfer_repo = MagicMock()
    mock_account_repo = MagicMock()

    service = TransferService(mock_transfer_repo, mock_account_repo)

    with pytest.raises(ValueError, match=error):
        await service.add_transfer(transfer.to_dict())


@pytest.mark.asyncio
async def test_delete_transfer() -> None:
    mock_transfer_repo = MagicMock()
    mock_account_repo = MagicMock()

    service = TransferService(mock_transfer_repo, mock_account_repo)

    await service.delete_transfer(1)

    mock_transfer_repo.delete.assert_called_once_with(1)
