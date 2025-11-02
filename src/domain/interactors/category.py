from typing import Iterator

from src.domain.entities import Category
from src.domain.interfaces import CategoryDataProvider


class CategoryInteractor:
    def __init__(self, data_provider: CategoryDataProvider):
        self.data_provider = data_provider

    def create_category(self, c: Category) -> Category:
        return self.data_provider.create_category(c)

    def get_category(self, cid: int) -> Category:
        return self.data_provider.get_category(cid)

    def get_categories(self, limit: int, offset: int = 0) -> Iterator[Category]:
        return self.data_provider.get_categories(limit, offset)

    def update_category(self, c: Category) -> Category:
        return self.data_provider.update_category(c)

    def remove_category(self, cid: int) -> Category:
        return self.data_provider.remove_category(cid)
