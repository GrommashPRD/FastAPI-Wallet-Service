from fastapi import APIRouter, HTTPException

from app.api.handlers.auth.schemas import SUser
from app.auth.dependencies import CurrentUserDep
from app.database import async_session_maker
from app.api.handlers.wallets import schemas
from app.usecase.wallets import operations_usecase as usecase
from app.usecase.wallets import exceptions as wallet_exceptions
from app.usecase.auth import exceptions as auth_exceptions

from app.logger import logger

router = APIRouter()


@router.post("/{wallet_uuid}/operation/")
async def operation_with_wallet(
        wallet_uuid: str,
        request: schemas.SOperationRequest,
        user: SUser = CurrentUserDep
):
    async with async_session_maker() as session:
        try:
            await usecase.update_wallet_balance(
                session,
                wallet_uuid,
                request,
                user
            )
        except wallet_exceptions.WalletNotFound:
            logger.warning(
                "Wallet with id %s not found"
                % wallet_uuid
            )
            raise HTTPException(
                detail="Wallet not found",
                status_code=400
            )
        except wallet_exceptions.InsufficientFunds:
            logger.warning(
                "Insufficient funds in the balance on wallet %s"
                % wallet_uuid
            )
            raise HTTPException(
                detail="Insufficient funds in the balance",
                status_code=400
            )
        except auth_exceptions.UserNotAuthorized:
            logger.warning(
                "Need authorize for a withdraw operation"
            )
            raise HTTPException(
                detail="Need authorize for withdraw operation",
                status_code=401
            )

        return {
            "message": "OK"
        }
