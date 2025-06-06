from fastapi import APIRouter, Depends
from middlewares.authorization import auth_check


from .address import router as address_router
from .categories import router as categories_router
# from .documents import router as documents_router
from .expenses import router as expenses_router
from .goods import router as goods_router
# from .goods_documents import router as goods_documents_router
from .role import router as role_router
from .person import router as person_router
from .auth import router as auth_router
from .type import router as type_router
from .users import router as users_router
from .expense_categories import router as expense_categories_router
from .image_loader import router as image_loader_router


router = APIRouter()

router.include_router(address_router, dependencies=[Depends(auth_check)])
router.include_router(auth_router)
router.include_router(categories_router, dependencies=[Depends(auth_check)])
# router.include_router(documents_router, dependencies=[Depends(auth_check)])
router.include_router(expenses_router, dependencies=[Depends(auth_check)])
router.include_router(goods_router, dependencies=[Depends(auth_check)])
# router.include_router(goods_documents_router, dependencies=[Depends(auth_check)])
router.include_router(expense_categories_router, dependencies=[Depends(auth_check)])
router.include_router(role_router, dependencies=[Depends(auth_check)])
router.include_router(users_router, dependencies=[Depends(auth_check)])
router.include_router(type_router, dependencies=[Depends(auth_check)])
router.include_router(person_router, dependencies=[Depends(auth_check)])
router.include_router(image_loader_router, dependencies=[Depends(auth_check)])


