from solution.repository.base_repository import BaseRepository
from solution.models.categories import Category
from typing import List, Any, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from solution.database import async_session_maker


def _category_to_dict(category: Category) -> dict[str, Any]:
    return {"id": category.id, "name": category.name, "type": category.type}


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
                    name=category_data["name"], type=category_data["type"]
                )

                if category is None:
                    raise ValueError("Category cannot be None")
                if not category.name or not category.name.strip():
                    raise ValueError("Category name cannot be empty")

                await self._check_if_exists(category)

                create = await self.category_repository.create(session, category)
            return _category_to_dict(create)

    async def delete_category(self, category_id: int) -> None:
        async with self.session_maker() as session:
            async with session.begin():
                await self.category_repository.delete(session, category_id)

    async def _check_if_exists(self, category: Category) -> None:
        async with self.session_maker() as session:
            existing_categories = await self.category_repository.get_all(session)
            for existing in existing_categories:
                if existing.name == category.name and existing.type == category.type:
                    raise ValueError("Category already exists")
