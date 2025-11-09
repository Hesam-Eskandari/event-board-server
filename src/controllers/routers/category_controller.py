import uuid

from fastapi import APIRouter, HTTPException, status, Response
from fastapi_utils.cbv import cbv

from src.controllers.dtos import CategoryReadDTO, CategoryCreateDTO, CategoryPatchDTO
from src.domain.exceptions import CategoryNotFoundException
from src.domain.interactors import CategoryInteractor
from src.services import PgDataBase

router = APIRouter()

@cbv(router)
class CategoryController:
    @router.get('/categories/')
    async def read_categories(self, limit: int = 0, offset: int = 0):
        interactor = CategoryInteractor(PgDataBase())
        try:
            categories = interactor.get_categories(limit, offset)
        except CategoryNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return [CategoryReadDTO.from_entity(category) for category in categories]

    @router.get('/categories/{category_id}', status_code=status.HTTP_200_OK, response_model=CategoryReadDTO)
    async def read_category(self, category_id: str):
        try:
            cid = uuid.UUID(category_id)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid category id')

        interactor = CategoryInteractor(PgDataBase())
        try:
            category = interactor.get_category(cid)
        except CategoryNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return CategoryReadDTO.from_entity(category)

    @router.post('/categories/', status_code=status.HTTP_201_CREATED, response_model=CategoryReadDTO)
    async def create_category(self, c: CategoryCreateDTO):
        category = c.to_entity()
        interactor = CategoryInteractor(PgDataBase())
        try:
            category_saved = interactor.create_category(category)
        except CategoryNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return CategoryReadDTO.from_entity(category_saved)

    @router.delete('/categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
    async def delete_category(self, category_id: str):
        try:
            cid = uuid.UUID(category_id)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid category id')

        interactor = CategoryInteractor(PgDataBase())
        try:
            _ = interactor.remove_category(cid)
        except CategoryNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @router.patch('/categories/{category_id}', status_code=status.HTTP_200_OK, response_model=CategoryReadDTO)
    async def patch_category(self, category_id: str, dto: CategoryPatchDTO):
        try:
            cid = uuid.UUID(category_id)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid category id')
        interactor = CategoryInteractor(PgDataBase())
        try:
            old_entity = interactor.get_category(cid)
        except CategoryNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')

        entity = dto.to_entity(old_entity)
        try:
            _ = interactor.update_category(entity)
        except CategoryNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return CategoryReadDTO.from_entity(entity)
