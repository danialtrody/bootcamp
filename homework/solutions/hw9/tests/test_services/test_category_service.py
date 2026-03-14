from typing import Any, Dict, List

import pytest
from unittest.mock import MagicMock, AsyncMock
from solution.services.category_service import CategoryService
from solution.models.categories import Category


@pytest.fixture
def category_service() -> CategoryService:

    category_repository = MagicMock()

    session = MagicMock()
    session_maker = MagicMock()
    session_maker.return_value.__aenter__.return_value = session

    service = CategoryService(
        category_repository=category_repository, session_maker=session_maker
    )

    return service


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "category_data, expected",
    [
        ([], []),
        (
            [Category(id=1, name="Salary", type="income")],
            [{"id": 1, "name": "Salary", "type": "income"}],
        ),
        (
            [
                Category(id=1, name="Salary", type="income"),
                Category(id=2, name="Freelance", type="income"),
            ],
            [
                {"id": 1, "name": "Salary", "type": "income"},
                {"id": 2, "name": "Freelance", "type": "income"},
            ],
        ),
        (
            [
                Category(id=1, name="Salary", type="income"),
                Category(id=2, name="Freelance", type="income"),
                Category(id=3, name="Rent", type="expense"),
            ],
            [
                {"id": 1, "name": "Salary", "type": "income"},
                {"id": 2, "name": "Freelance", "type": "income"},
                {"id": 3, "name": "Rent", "type": "expense"},
            ],
        ),
        (
            [
                Category(id=1, name="Salary", type="income"),
                Category(id=2, name="Freelance", type="income"),
                Category(id=3, name="Rent", type="expense"),
                Category(id=4, name="Groceries", type="expense"),
                Category(id=5, name="Utilities", type="expense"),
            ],
            [
                {"id": 1, "name": "Salary", "type": "income"},
                {"id": 2, "name": "Freelance", "type": "income"},
                {"id": 3, "name": "Rent", "type": "expense"},
                {"id": 4, "name": "Groceries", "type": "expense"},
                {"id": 5, "name": "Utilities", "type": "expense"},
            ],
        ),
    ],
)
async def test_get_all_categories(
    category_service: CategoryService,
    category_data: List[Category],
    expected: List[Dict[str, Any]],
) -> None:
    service = category_service
    service.category_repository.get_all = AsyncMock(return_value=category_data)

    result = await service.get_all_categories()
    assert result == expected


@pytest.mark.asyncio
async def test_add_category_success(category_service: CategoryService) -> None:
    service = category_service

    category_data = {"name": "TEST", "type": "expense"}

    mock_category = MagicMock()
    mock_category.id = 1
    mock_category.name = "TEST"
    mock_category.type = "expense"

    service.category_repository.get_all = AsyncMock(return_value=[])
    service.category_repository.create = AsyncMock(return_value=mock_category)

    result = await service.add_category(category_data)

    assert result == {"id": 1, "name": "TEST", "type": "expense"}


@pytest.mark.asyncio
async def test_add_category_fail(category_service: CategoryService) -> None:
    service = category_service

    category_data = {"name": "TEST", "type": "expense"}
    mock_category = MagicMock()
    mock_category.id = 1
    mock_category.name = "TEST"
    mock_category.type = "expense"

    service.category_repository.get_all = AsyncMock(return_value=[mock_category])
    service.category_repository.create = AsyncMock(return_value=mock_category)

    with pytest.raises(ValueError, match="Category already exists"):
        await service.add_category(category_data)


@pytest.mark.asyncio
async def test_delete_category(category_service: CategoryService) -> None:
    service = category_service

    service.category_repository.delete = AsyncMock()
    await service.delete_category(50)
    service.category_repository.delete.assert_awaited_once()
