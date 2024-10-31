from fastapi import APIRouter, Depends
from middlewares.authorization import auth_check


from .address import router as address_router
from .categories import router as categories_router
from .documents import router as documents_router
from .expenses import router as expenses_router
from .goods import router as goods_router
from .goods_documents import router as goods_documents_router
from .status import router as status_router
from .users import router as users_router


router = APIRouter()

router.include_router(address_router, dependencies=[Depends(auth_check)])
router.include_router(auth_router)
router.include_router(categories_router, dependencies=[Depends(auth_check)])
router.include_router(documents_router, dependencies=[Depends(auth_check)])
router.include_router(expenses_router, dependencies=[Depends(auth_check)])
router.include_router(goods_router, dependencies=[Depends(auth_check)])
router.include_router(goods_documents_router, dependencies=[Depends(auth_check)])
router.include_router(status_router, dependencies=[Depends(auth_check)])
router.include_router(users_router, dependencies=[Depends(auth_check)])
