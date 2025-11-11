from typing import AsyncGenerator
from uuid import UUID

from sqlalchemy import select, update, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import Category
from src.domain.exceptions import CategoryNotFoundException
from src.domain.interfaces import CategoryDataProvider
from src.services.postgres.models import CategoryModel
from src.services.postgres.pg_base import PgBase


class PgCategoryDataProvider(PgBase, CategoryDataProvider):
    async def create_category(self, c: Category) -> Category:
        session: AsyncSession
        async with self._setup_connection() as session:
            try:
                category_model: CategoryModel = CategoryModel.from_entity(c)
                session.add(category_model)
                await session.commit()
                await session.refresh(category_model)
                return category_model.to_entity()
            except Exception as err:
                print("db error", err)

    async def get_category(self, cid: UUID) -> Category:
        session: AsyncSession
        async with self._setup_connection() as session:
            stmt = select(CategoryModel).where(CategoryModel.is_deleted.is_(False)).where(CategoryModel.id == cid)
            model: CategoryModel | None = await session.scalar(stmt)
            if model is None:
                raise CategoryNotFoundException(f"category {cid} not found")
            return model.to_entity()

    async def get_categories(self, limit: int, offset: int = 0) -> AsyncGenerator["Category", None]:
        session: AsyncSession
        async with self._setup_connection() as session:
            try:
                stmt = select(CategoryModel).where(CategoryModel.is_deleted.is_(False)).limit(limit).offset(offset)
                models: ScalarResult[CategoryModel] = await session.scalars(stmt)
                for model in models.all():
                    print(model)
                    yield model.to_entity()
            except Exception as err:
                print("db error", err)

    async def update_category(self, c: Category) -> Category:
        session: AsyncSession
        async with self._setup_connection() as session:
            model = CategoryModel.from_entity(c)
            stmt = (
                update(CategoryModel)
                .where(CategoryModel.is_deleted.is_(False))
                .where(CategoryModel.id == c.id)
                .values(**model.to_dict(exclude_id=True, exclude_fields=['is_deleted']))
                .returning(CategoryModel)
            )
            result = await session.execute(stmt)
            updated_model: CategoryModel | None = result.scalar_one_or_none()
            if updated_model is None:
                raise CategoryNotFoundException(f"category {c.id} not found")
            await session.commit()
            return updated_model.to_entity()

    async def remove_category(self, cid: UUID) -> Category:
        session: AsyncSession
        async with self._setup_connection() as session:
            stmt = (
                update(CategoryModel)
                .where(CategoryModel.is_deleted.is_(False))
                .where(CategoryModel.id == cid)
                .values(is_deleted=True)
                .returning(CategoryModel)
            )

            result = await session.execute(stmt)
            deleted_model: CategoryModel | None = result.scalar_one_or_none()
            if deleted_model is None:
                raise CategoryNotFoundException(f"category {cid} not found")

            await session.commit()
            return deleted_model.to_entity()
