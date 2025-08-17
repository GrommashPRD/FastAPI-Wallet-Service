from fastapi import APIRouter

from app.api.handlers.wallets.balance_details import router as details_router
from app.api.handlers.wallets.crete_new_wallet import router as create_wallet_router
from app.api.handlers.wallets.get_wallet_balance import router as get_wallet_balance_router
from app.api.handlers.wallets.operations_with_wallet import router as operations_router
from app.api.handlers.wallets.get_user_wallet import router as user_wallet_router

router = APIRouter(
    prefix="/wallets",
    tags=["Кошельки"]
)

router.include_router(details_router)
router.include_router(create_wallet_router)
router.include_router(get_wallet_balance_router)
router.include_router(operations_router)
router.include_router(user_wallet_router)
