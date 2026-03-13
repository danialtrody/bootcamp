from typing import List, Any, Dict, Optional
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from solution.repository.base_repository import BaseRepository
from solution.models.categories import Category
from solution.database import async_session_maker


KEY_NAME = "name"
KEY_TYPE = "type"
EXPENSE = "expense"
INCOME = "income"


DEFAULT_CATEGORIES: tuple[dict[str, str], ...] = (
    {KEY_NAME: "Salary", KEY_TYPE: INCOME},
    {KEY_NAME: "Freelance", KEY_TYPE: INCOME},
    {KEY_NAME: "Rent", KEY_TYPE: EXPENSE},
    {KEY_NAME: "Groceries", KEY_TYPE: EXPENSE},
    {KEY_NAME: "Utilities", KEY_TYPE: EXPENSE},
    {KEY_NAME: "Entertainment", KEY_TYPE: EXPENSE},
)


def _category_to_dict(category: Category) -> dict[str, Any]:
    return {"id": category.id, KEY_NAME: category.name, KEY_TYPE: category.type}


class CategoryService:

    def __init__(
        self,
        category_repository: BaseRepository[Category],
        session_maker: Optional[async_sessionmaker[AsyncSession]] = None,
    ):
        self.category_repository = category_repository
        self.session_maker = session_maker or async_session_maker

    async def get_all_categories(self) -> List[dict[Any, Any]]:
        async with self.session_maker() as session:
            categories = await self.category_repository.get_all(session)
            return [_category_to_dict(category) for category in categories]

    async def add_category(self, category_data: Dict[str, Any]) -> Dict[str, Any]:
        async with self.session_maker() as session:
            async with session.begin():
                category = Category(
                    name=category_data[KEY_NAME], type=category_data[KEY_TYPE]
                )

                if category is None:
                    raise ValueError("Category cannot be None")
                if not category.name or not category.name.strip():
                    raise ValueError("Category name cannot be empty")

                await self._check_if_exists(category)

                created = await self.category_repository.create(session, category)
                return _category_to_dict(created)

    async def delete_category(self, category_id: int) -> None:
        async with self.session_maker() as session:
            async with session.begin():
                await self.category_repository.delete(session, category_id)

    async def seed_default_categories(self) -> None:
        async with self.session_maker() as session:
            async with session.begin():
                categories = await self.category_repository.get_all(session)
                if categories:
                    return

                await asyncio.gather(
                    *[
                        self.category_repository.create(
                            session, Category(name=data[KEY_NAME], type=data[KEY_TYPE])
                        )
                        for data in DEFAULT_CATEGORIES
                    ]
                )

    async def _check_if_exists(self, category: Category) -> None:
        async with self.session_maker() as session:
            existing_categories = await self.category_repository.get_all(session)
            for existing in existing_categories:
                if existing.name == category.name and existing.type == category.type:
                    raise ValueError("Category already exists")
