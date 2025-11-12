from fastapi import APIRouter, HTTPException, status, Response
from fastapi_utils.cbv import cbv

from src.controllers.dtos import CategoryReadDTO, CategoryCreateDTO, CategoryPatchDTO
from src.controllers.routers import ErrorHandler
from src.domain.interactors import CategoryInteractor
from src.domain.interfaces import CategoryDataProvider
from src.services import PgCategoryDataProvider

router = APIRouter()

@cbv(router)
class CategoryController:

    def __init__(self):
        self._data_provider: CategoryDataProvider = PgCategoryDataProvider()

    @router.post('/categories/', status_code=status.HTTP_201_CREATED, response_model=CategoryReadDTO)
    async def create_category(self, c: CategoryCreateDTO):
        entity = c.to_entity()
        interactor = CategoryInteractor(self._data_provider)
        created_entity = await ErrorHandler.handle_await_async(interactor.create_category(entity))
        return CategoryReadDTO.from_entity(created_entity)

    @router.get('/categories/')
    async def read_categories(self, limit: int = 0, offset: int = 0):
        interactor = CategoryInteractor(self._data_provider)
        return [CategoryReadDTO.from_entity(category) async for category in \
                ErrorHandler.handle_await_all_async(interactor.get_categories(limit, offset))]

    @router.get('/categories/{category_id}', status_code=status.HTTP_200_OK, response_model=CategoryReadDTO)
    async def read_category(self, category_id: str):
        cid = ErrorHandler.handle_str_to_uuid(category_id, f"invalid category id {category_id}")
        interactor = CategoryInteractor(self._data_provider)
        category = await ErrorHandler.handle_await_async(interactor.get_category(cid))
        return CategoryReadDTO.from_entity(category)

    @router.patch('/categories/{category_id}', status_code=status.HTTP_200_OK, response_model=CategoryReadDTO)
    async def patch_category(self, category_id: str, dto: CategoryPatchDTO):
        cid = ErrorHandler.handle_str_to_uuid(category_id, f"invalid category id {category_id}")
        interactor = CategoryInteractor(self._data_provider)
        old_entity = await ErrorHandler.handle_await_async(interactor.get_category(cid))
        entity = dto.to_entity(old_entity)
        if entity == old_entity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='category update failed. no field is changed')
        updated_entity = await ErrorHandler.handle_await_async(interactor.update_category(entity))
        return CategoryReadDTO.from_entity(updated_entity)

    @router.delete('/categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
    async def delete_category(self, category_id: str):
        cid = ErrorHandler.handle_str_to_uuid(category_id, f"invalid category id {category_id}")
        interactor = CategoryInteractor(self._data_provider)
        _ = await ErrorHandler.handle_await_async(interactor.remove_category(cid))
        return Response(status_code=status.HTTP_204_NO_CONTENT)
