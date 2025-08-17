from fastapi import APIRouter, HTTPException
from app.database import async_session_maker
from app.auth.dependencies import CurrentUserDep

from app.api.handlers.auth import schemas
from app.usecase.wallets import usecase
from app.usecase.wallets import exceptions as wallet_exceptions
from app.usecase.auth import exceptions as auth_exceptions

from app.logger import logger

router = APIRouter()


@router.get("/{wallet_uuid}")
async def get_wallet_balance(
        wallet_uuid: str,
        user: schemas.SUser = CurrentUserDep,
):
    """
    Only wallet balance endpoint.
    Only authorized users with a wallet.
    :param wallet_uuid: str
    :param user: SUser data, id и username.
    :return:
    """
    async with async_session_maker() as session:

        try:
            wallet = await usecase.get_user_wallet(
                session,
                user,
                wallet_uuid
            )
        except auth_exceptions.UserNotAuthorized:
            logger.warning("User not authorize for see wallet balance")
            raise HTTPException(
                detail="Need authorization for see wallet balance",
                status_code=401
            )
        except wallet_exceptions.WalletNotFound:
            logger.warning("Wallet with id %s not found" % wallet_uuid)
            raise HTTPException(
                detail="Wallet with id: %s not found or it's not your wallet"
                % wallet_uuid,
                status_code=404
            )
        except wallet_exceptions.WalletDontExist:
            logger.warning("User %s cant see this wallet %s balance",
                           user.id,
                           wallet_uuid
                           )
            raise HTTPException(
                detail="This wallet is not your",
                status_code=404
            )

        return {
            "message": "OK",
            "wallet balance": wallet.balance
        }
