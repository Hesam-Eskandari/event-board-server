from fastapi import APIRouter, HTTPException, status, Response
from fastapi_utils.cbv import cbv

from src.controllers.dtos import CategoryReadDTO, CategoryCreateDTO, CategoryPatchDTO
from src.controllers.routers import CategoryErrorHandler, UUIDErrorHandler
from src.domain.interactors import CategoryInteractor
from src.services import DataBaseMock

router = APIRouter()

@cbv(router)
class CategoryController:

    @router.post('/categories/', status_code=status.HTTP_201_CREATED, response_model=CategoryReadDTO)
    async def create_category(self, c: CategoryCreateDTO):
        entity = c.to_entity()
        interactor = CategoryInteractor(DataBaseMock())
        _ = await CategoryErrorHandler.handle_create_async(interactor.create_category(entity))
        return CategoryReadDTO.from_entity(entity)

    @router.get('/categories/')
    async def read_categories(self, limit: int = 0, offset: int = 0):
        interactor = CategoryInteractor(DataBaseMock())
        categories = await CategoryErrorHandler.handle_read_all_async(interactor.get_categories(limit, offset))
        return [CategoryReadDTO.from_entity(category) for category in categories]

    @router.get('/categories/{category_id}', status_code=status.HTTP_200_OK, response_model=CategoryReadDTO)
    async def read_category(self, category_id: str):
        cid = UUIDErrorHandler.handle_str_to_uuid(category_id, f"invalid category id {category_id}")
        interactor = CategoryInteractor(DataBaseMock())
        category = await CategoryErrorHandler.handle_read_async(interactor.get_category(cid))
        return CategoryReadDTO.from_entity(category)

    @router.patch('/categories/{category_id}', status_code=status.HTTP_200_OK, response_model=CategoryReadDTO)
    async def patch_category(self, category_id: str, dto: CategoryPatchDTO):
        cid = UUIDErrorHandler.handle_str_to_uuid(category_id, f"invalid category id {category_id}")
        interactor = CategoryInteractor(DataBaseMock())
        old_entity = await CategoryErrorHandler.handle_read_async(interactor.get_category(cid))
        entity = dto.to_entity(old_entity)
        if entity == old_entity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='category update failed. no field is changed')
        _ = await CategoryErrorHandler.handle_update_async(interactor.update_category(entity))
        return CategoryReadDTO.from_entity(entity)

    @router.delete('/categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
    async def delete_category(self, category_id: str):
        cid = UUIDErrorHandler.handle_str_to_uuid(category_id, f"invalid category id {category_id}")
        interactor = CategoryInteractor(DataBaseMock())
        _ = await CategoryErrorHandler.handle_delete_async(interactor.remove_category(cid))
        return Response(status_code=status.HTTP_204_NO_CONTENT)
