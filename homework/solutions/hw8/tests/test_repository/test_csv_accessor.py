from unittest.mock import MagicMock

import pytest
from solution.repository.base_repository import BaseRepository
from solution.models.categories import Category


def test_create_success() -> None:
    mock_accessor = MagicMock()
    repository = BaseRepository(mock_accessor, Category)
    mock_accessor.read.return_value = []

    category = Category(id=1, name="TEST", type="income")

    result = repository.create(category)
    assert result == category
    mock_accessor.read.assert_called_once()
    mock_accessor.write.assert_called_once_with(
        [{"id": 1, "name": "TEST", "type": "income"}]
    )


def test_get_success() -> None:
    mock_accessor = MagicMock()
    repository = BaseRepository(mock_accessor, Category)

    mock_accessor.read.return_value = [{"id": 1, "name": "TEST", "type": "income"}]
    result = repository.get(1)
    assert result.id == 1
    assert result.name == "TEST"
    assert result.type == "income"

    mock_accessor.read.assert_called_once()


def test_get_fail() -> None:
    mock_accessor = MagicMock()
    repository = BaseRepository(mock_accessor, Category)
    with pytest.raises(ValueError, match="Category: Entity with ID=1 was not found"):
        repository.get(1)


def test_get_all() -> None:
    mock_accessor = MagicMock()
    repository = BaseRepository(mock_accessor, Category)

    mock_accessor.read.return_value = [
        {"id": 1, "name": "TEST", "type": "income"},
        {"id": 2, "name": "TEST2", "type": "income2"},
    ]
    result = repository.get_all()
    assert len(result) == 2
    assert result[0].id == 1
    assert result[0].name == "TEST"
    assert result[0].type == "income"

    assert result[1].id == 2
    assert result[1].name == "TEST2"
    assert result[1].type == "income2"

    mock_accessor.read.assert_called_once()


def test_update_success() -> None:
    mock_accessor = MagicMock()
    repository = BaseRepository(mock_accessor, Category)

    mock_accessor.read.return_value = [{"id": 1, "name": "TEST", "type": "income"}]
    updated = Category(id=1, name="updated", type="updated")

    result = repository.update(updated)
    assert result.id == 1
    assert result.name == "updated"
    assert result.type == "updated"

    mock_accessor.read.assert_called_once()
    mock_accessor.write.assert_called_once_with(
        [{"id": 1, "name": "updated", "type": "updated"}]
    )


def test_update_fail() -> None:
    mock_accessor = MagicMock()
    repository = BaseRepository(mock_accessor, Category)
    updated = Category(id=1, name="updated", type="updated")

    with pytest.raises(ValueError, match="Category: Entity with ID=1 was not found"):
        repository.update(updated)


def test_delete_success() -> None:
    mock_accessor = MagicMock()
    repository = BaseRepository(mock_accessor, Category)

    mock_accessor.read.return_value = [{"id": 1, "name": "TEST", "type": "income"}]

    repository.delete(1)

    mock_accessor.read.assert_called_once()


def test_delete_fail() -> None:
    mock_accessor = MagicMock()
    repository = BaseRepository(mock_accessor, Category)
    mock_accessor.read.return_value = [{"id": 1, "name": "TEST", "type": "income"}]

    with pytest.raises(ValueError, match="Category: Entity with ID=2 was not found"):
        repository.delete(2)
