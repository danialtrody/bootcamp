from solution.repository.base_repository import BaseRepository
from solution.models.categories import Category, CategoryType
from typing import List, Any, Dict


NAME = "name"
TYPE = "type"

DEFAULT_CATEGORIES = (
    {NAME: "Salary", TYPE: "income"},
    {NAME: "Freelance", TYPE: "income"},
    {NAME: "Rent", TYPE: "expense"},
    {NAME: "Groceries", TYPE: "expense"},
    {NAME: "Utilities", TYPE: "expense"},
)


class CategoryService:

    def __init__(self, category_repository: BaseRepository[Category]):
        self.category_repository = category_repository

    async def get_all_categories(self) -> List[dict[Any, Any]]:
        categories = self.category_repository.get_all()
        return [category.to_dict() for category in categories]

    async def add_category(self, category_data: Dict[str, Any]) -> Dict[str, Any]:

        category = Category(name=category_data["name"], type=category_data["type"])

        if category is None:
            raise ValueError("Category cannot be None")
        if not category.name or not category.name.strip():
            raise ValueError("Category name cannot be empty")

        self._check_if_exists(category)

        create = self.category_repository.create(category)
        return create.to_dict()

    async def delete_category(self, category_id: int) -> None:
        self.category_repository.delete(category_id)

    async def seed_default_categories(self) -> None:
        categories = self.category_repository.get_all()

        if not categories:
            for category_data in DEFAULT_CATEGORIES:
                category = Category(
                    name=category_data["name"],
                    type=CategoryType(category_data["type"]),
                )
                self.category_repository.create(category)

    def _check_if_exists(self, category: Category) -> None:
        existing_categories = self.category_repository.get_all()
        for existing in existing_categories:
            if existing.name == category.name and existing.type == category.type:
                raise ValueError("Category already exists")
