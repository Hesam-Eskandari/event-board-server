import uuid

from fastapi import HTTPException, status


class UUIDErrorHandler:

    @staticmethod
    def handle_str_to_uuid(uuid_str: str, err_message: str | None = None) -> uuid.UUID:
        err_message = err_message if err_message is not None else f'invalid id: {uuid_str}'
        try:
            uid = uuid.UUID(uuid_str)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err_message)
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'failed reading uuid from {uuid_str}')
        return uid
