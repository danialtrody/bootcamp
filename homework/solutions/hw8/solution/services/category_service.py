from solution.repository.base_repository import BaseRepository
from solution.models.categories import Category, CategoryType
from typing import List


class CategoryService:

    def __init__(self, category_repository: BaseRepository[Category]):
        self.category_repository = category_repository

    def get_all_categories(self) -> List[Category]:
        return self.category_repository.get_all()

    def add_category(self, category: Category) -> Category:

        if not category.name.strip():
            raise ValueError("Category name cannot be empty")

        if not isinstance(category.type, CategoryType):
            raise ValueError("Invalid category type")

        return self.category_repository.create(category)

    def delete_category(self, category_id: int) -> None:
        self.category_repository.delete(category_id)
