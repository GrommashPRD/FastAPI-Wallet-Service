from fastapi import APIRouter, HTTPException
from app.database import async_session_maker
from app.auth.dependencies import CurrentUserDep

from app.api.handlers.auth import schemas
from app.usecase.wallets import usecase
from app.usecase.wallets import exceptions as wallet_exceptions
from app.usecase.auth import exceptions as auth_exceptions

from app.logger import logger

router = APIRouter()


@router.get("/my/")
async def get_user_wallet(
        user: schemas.SUser = CurrentUserDep,
):
    """
    Wallet info endpoint.
    Only authorized users with a wallet.
    :param user: SUser data, id и username.
    :return: message, wallet id и wallet balance.
    """
    async with async_session_maker() as session:
        try:
            wallet = await usecase.get_user_wallet(
                session,
                user
            )
        except auth_exceptions.UserNotAuthorized:
            logger.warning("Need auth for create a new wallet")
            raise HTTPException(
                detail="You need authorize for see wallets",
                status_code=401
            )
        except wallet_exceptions.WalletDontExist:
            logger.warning("User - %s dont have wallet" % user.id)
            raise HTTPException(
                detail="You are dont have wallets",
                status_code=404
            )

    return {
        "message": "OK",
        "wallet id": wallet.id,
        "wallet balance": wallet.balance
    }
