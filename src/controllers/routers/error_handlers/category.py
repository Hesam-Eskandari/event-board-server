from typing import Coroutine, Any, Iterator, AsyncGenerator

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
        except Exception as err:
            print(err)
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
    async def handle_read_all_async(categories_async: AsyncGenerator[Category, None]) -> AsyncGenerator[Category, None]:
        try:
            async for category in categories_async:
                yield category
        except CategoryNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')

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
