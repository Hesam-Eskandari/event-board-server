from fastapi import APIRouter, HTTPException
from fastapi_utils.cbv import cbv

from src.controllers.dtos import CategoryDTO
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
            raise HTTPException(status_code=404, detail=str(err))
        except Exception:
            raise HTTPException(status_code=500, detail='unexpected error happened')
        return [CategoryDTO.from_entity(category) for category in categories]

    @router.get('/categories/{category_id}')
    async def read_category(self, category_id: int):
        interactor = CategoryInteractor(PgDataBase())
        try:
            category = interactor.get_category(category_id)
        except CategoryNotFoundException as err:
            raise HTTPException(status_code=404, detail=str(err))
        except Exception:
            raise HTTPException(status_code=500, detail='unexpected error happened')
        return CategoryDTO.from_entity(category)

    @router.post('/categories/')
    async def create_category(self, c: CategoryDTO):
        category = c.to_entity(True)
        interactor = CategoryInteractor(PgDataBase())
        try:
            category_saved = interactor.create_category(category)
        except CategoryNotFoundException as err:
            raise HTTPException(status_code=404, detail=str(err))
        except Exception:
            raise HTTPException(status_code=500, detail='unexpected error happened')
        return CategoryDTO.from_entity(category_saved)

    @router.delete('/categories/{category_id}')
    async def delete_category(self, category_id: int):
        interactor = CategoryInteractor(PgDataBase())
        try:
            category_saved = interactor.remove_category(category_id)
        except CategoryNotFoundException as err:
            raise HTTPException(status_code=404, detail=str(err))
        except Exception:
            raise HTTPException(status_code=500, detail='unexpected error happened')
        return CategoryDTO.from_entity(category_saved)

    @router.put('/categories/')
    async def update_category(self, c: CategoryDTO):
        category = c.to_entity(False)
        interactor = CategoryInteractor(PgDataBase())
        try:
            category_saved = interactor.update_category(category)
        except CategoryNotFoundException as err:
            raise HTTPException(status_code=404, detail=str(err))
        except Exception:
            raise HTTPException(status_code=500, detail='unexpected error happened')
        return CategoryDTO.from_entity(category_saved)
