from unittest.mock import MagicMock

import pytest
from solution.services.category_service import CategoryService
from solution.models.categories import Category, CategoryType
from typing import List, Dict


NAME = "TEST"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_data, output",
    [
        ([], []),
        (
            [Category(id=1, name=NAME, type=CategoryType.INCOME)],
            [{"id": 1, "name": NAME, "type": CategoryType.INCOME}],
        ),
        (
            [
                Category(id=1, name=NAME, type=CategoryType.INCOME),
                Category(id=2, name="TEST2", type=CategoryType.INCOME),
            ],
            [
                {"id": 1, "name": "TEST", "type": CategoryType.INCOME},
                {"id": 2, "name": "TEST2", "type": CategoryType.INCOME},
            ],
        ),
    ],
)
async def test_get_all_categories(test_data: List[Dict], output: List[Dict]) -> None:
    mock_repository = MagicMock()
    mock_repository.get_all.return_value = test_data
    service = CategoryService(mock_repository)
    result = await service.get_all_categories()

    assert result == output
    mock_repository.get_all.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_data",
    [
        Category(id=1, name="TEST", type=CategoryType.INCOME),
        Category(id=2, name="TEST2", type=CategoryType.EXPENSE),
    ],
)
async def test_add_category_success(test_data: Category) -> None:
    mock_repository = MagicMock()
    mock_repository.create.return_value = test_data
    service = CategoryService(mock_repository)
    result = await service.add_category(test_data.to_dict())

    assert result == test_data.to_dict()


@pytest.mark.asyncio
async def test_delete_category() -> None:
    mock_repository = MagicMock()
    service = CategoryService(mock_repository)
    mock_repository.delete.return_value = None
    await service.delete_category(1)

    mock_repository.delete.assert_called_once_with(1)
