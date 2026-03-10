from unittest.mock import MagicMock

import pytest
from solution.services.category_service import CategoryService
from solution.models.categories import Category, CategoryType
from typing import List, Dict


@pytest.mark.parametrize(
    "test_data, output",
    [
        ([], []),
        (
            [{"id": 1, "name": "TEST", "type": CategoryType.INCOME}],
            [{"id": 1, "name": "TEST", "type": CategoryType.INCOME}],
        ),
        (
            [
                {"id": 1, "name": "TEST", "type": CategoryType.INCOME},
                {"id": 2, "name": "TEST2", "type": CategoryType.INCOME},
            ],
            [
                {"id": 1, "name": "TEST", "type": CategoryType.INCOME},
                {"id": 2, "name": "TEST2", "type": CategoryType.INCOME},
            ],
        ),
    ],
)
def test_get_all_categories(test_data: List[Dict], output: List[Dict]) -> None:
    mock_repository = MagicMock()
    mock_repository.get_all.return_value = test_data
    service = CategoryService(mock_repository)
    result = service.get_all_categories()

    assert result == output
    mock_repository.get_all.assert_called_once()


@pytest.mark.parametrize(
    "test_data",
    [
        Category(id=1, name="TEST", type=CategoryType.INCOME),
        Category(id=2, name="TEST2", type=CategoryType.EXPENSE),
    ],
)
def test_add_category_success(test_data: Category) -> None:
    mock_repository = MagicMock()
    mock_repository.create.return_value = test_data
    service = CategoryService(mock_repository)
    result = service.add_category(test_data)

    assert result == test_data
    mock_repository.create.assert_called_once_with(test_data)


@pytest.mark.parametrize(
    "data, error",
    [
        (
            Category(id=1, name="", type=CategoryType.INCOME),
            "Category name cannot be empty",
        ),
    ],
)
def test_add_category_fail(data: Category, error: str) -> None:

    mock_repository = MagicMock()
    service = CategoryService(mock_repository)

    with pytest.raises(ValueError, match=error):
        service.add_category(data)


def test_delete_category() -> None:
    mock_repository = MagicMock()
    service = CategoryService(mock_repository)
    mock_repository.delete.return_value = None
    service.delete_category(1)

    mock_repository.delete.assert_called_once_with(1)
