from abc import ABC
from typing import AsyncGenerator
from uuid import UUID

from src.domain.entities import Category


class CategoryDataProvider(ABC):
    async def create_category(self, c: Category) -> Category:
        raise NotImplementedError('create_category is not implemented')

    async def get_category(self, cid: UUID) -> Category:
        raise NotImplementedError('get_category is not implemented')

    def get_categories(self, limit: int, offset: int = 0) -> AsyncGenerator["Category", None]:
        raise NotImplementedError('get_categories is not implemented')

    async def update_category(self, c: Category) -> Category:
        raise NotImplementedError('update_category is not implemented')

    async def remove_category(self, cid: UUID) -> Category:
        raise NotImplementedError('remove_category is not implemented')
