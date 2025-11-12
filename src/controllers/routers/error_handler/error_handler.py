from uuid import UUID
from typing import Coroutine, Any, TypeVar, Generic, AsyncGenerator

from fastapi import HTTPException, status

from src.domain.exceptions import RecordNotFoundException

T = TypeVar('T')

class ErrorHandler(Generic[T]):

    @staticmethod
    async def handle_await_async(entity_async: Coroutine[Any, Any, T]) -> T:
        try:
            entity = await entity_async
        except RecordNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except ConnectionError as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return entity

    @staticmethod
    async def handle_await_all_async(entities_async: AsyncGenerator[T, None]) -> AsyncGenerator[T, None]:
        try:
            async for entity in entities_async:
                yield entity
        except RecordNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except ConnectionError as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))
        except Exception as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')

    @staticmethod
    def handle_str_to_uuid(uuid_str: str, err_message: str | None = None) -> UUID:
        err_message = err_message if err_message is not None else f'invalid id: {uuid_str}'
        try:
            uid = UUID(uuid_str)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err_message)
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'failed reading uuid from {uuid_str}')
        return uid
