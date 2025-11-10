from typing import Coroutine, Any, Iterator

from fastapi import HTTPException, status

from src.domain.entities import Category
from src.domain.exceptions import CategoryNotFoundException


class CategoryErrorHandler:

    @staticmethod
    async def handle_create_async(category_async: Coroutine[Any, Any, Category]) -> Category:
        try:
            category = await category_async
        except CategoryNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return category

    @staticmethod
    async def handle_read_async(category_async: Coroutine[Any, Any, Category]) -> Category:
        try:
            category = await category_async
        except CategoryNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return category

    @staticmethod
    async def handle_read_all_async(categories_async: Coroutine[Any, Any, Iterator[Category]]) -> Iterator[Category]:
        try:
            categories = await categories_async
        except CategoryNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return categories

    @staticmethod
    async def handle_update_async(category_async: Coroutine[Any, Any, Category]) -> Category:
        try:
            category = await category_async
        except CategoryNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return category

    @staticmethod
    async def handle_delete_async(category_async: Coroutine[Any, Any, Category]) -> Category:
        try:
            category = await category_async
        except CategoryNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return category
