from typing import AsyncGenerator
from uuid import UUID

from src.domain.entities import Category
from src.domain.interfaces import CategoryDataProvider


class CategoryInteractor:
    def __init__(self, data_provider: CategoryDataProvider):
        self.data_provider = data_provider

    async def create_category(self, c: Category) -> Category:
        return await self.data_provider.create_category(c)

    async def get_category(self, cid: UUID) -> Category:
        return await self.data_provider.get_category(cid)

    async def get_categories(self, limit: int, offset: int = 0) -> AsyncGenerator["Category", None]:
        async for category in self.data_provider.get_categories(limit, offset):
            yield category

    async def update_category(self, c: Category) -> Category:
        return  await self.data_provider.update_category(c)

    async def remove_category(self, cid: UUID) -> Category:
        return await self.data_provider.remove_category(cid)
