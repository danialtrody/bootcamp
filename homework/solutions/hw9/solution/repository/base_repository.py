from typing import Generic, TypeVar, Type, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


EntityType = TypeVar("EntityType")


class BaseRepository(Generic[EntityType]):

    def __init__(self, model_type: Type[EntityType]):
        self._model_type = model_type

    async def create(self, session: AsyncSession, item: EntityType) -> EntityType:
        session.add(item)
        return item

    async def get(self, session: AsyncSession, item_id: int) -> EntityType:
        result = await session.get(self._model_type, item_id)
        if not result:
            modal_name = self._model_type.__name__
            raise ValueError(f"{modal_name}: Entity with ID={item_id} was not found")
        return result

    async def get_all(self, session: AsyncSession) -> List[EntityType]:
        result = await session.scalars(select(self._model_type))
        return list(result.all())

    async def update(self, session: AsyncSession, item: EntityType) -> EntityType:
        updated = await session.merge(item)
        return updated

    async def delete(self, session: AsyncSession, item_id: int) -> None:
        obj = await session.get(self._model_type, item_id)
        if not obj:
            modal_name = self._model_type.__name__
            raise ValueError(f"{modal_name}: Entity with ID={item_id} was not found")
        await session.delete(obj)

    async def exists(self, session: AsyncSession, item_id: int) -> bool:
        obj = await session.get(self._model_type, item_id)
        return obj is not None
