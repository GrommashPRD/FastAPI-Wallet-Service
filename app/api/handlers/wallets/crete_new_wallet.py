from fastapi import APIRouter, HTTPException
from app.database import async_session_maker
from app.auth.dependencies import CurrentUserDep
from app.api.handlers.auth import schemas
from app.usecase.wallets import usecase
from app.usecase.wallets import exceptions as wallet_exceptions
from app.usecase.auth import exceptions as auth_exceptions
from app.logger import logger

router = APIRouter()


@router.post("/create")
async def create_wallet(
        user: schemas.SUser = CurrentUserDep
):
    """
    Wallet create endpoint.
    Only authorized users.
    :param user: SUser data id username.
    :return: message и wallet id.
    """
    async with async_session_maker() as session:

        try:
            wallet = await usecase.create_new_wallet(
                user,
                session
            )
        except wallet_exceptions.UserAlreadyHaveWallet:
            logger.warning(
                "User - %s already have wallet"
                % user.id
            )
            raise HTTPException(
                detail="You are already have wallet",
                status_code=400
            )
        except auth_exceptions.UserNotAuthorized:
            logger.warning(
                "User need authorize for create wallet"
            )
            raise HTTPException(
                detail="You are need authorize for create a wallet",
                status_code=401
            )

    return {
        "message": "OK",
        "wallet id": wallet.id
    }
