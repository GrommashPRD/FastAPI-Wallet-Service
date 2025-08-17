from fastapi import APIRouter, HTTPException
from app.database import async_session_maker
from app.auth.dependencies import CurrentUserDep

from app.api.handlers.auth import schemas
from app.usecase.wallets import usecase
from app.usecase.wallets import exceptions as wallet_exceptions
from app.usecase.auth import exceptions as auth_exceptions
from app.logger import logger

router = APIRouter()


@router.get("/{wallet_uuid}/details")
async def get_wallet_details(
        wallet_uuid: str,
        user: schemas.SUser = CurrentUserDep,
):
    """
    Wallet details endpoint.
    Only authorized users with a wallet.
    :param wallet_uuid: wallet.id.
    :param user: SUser data, id и username.
    :return: message и details.
    """
    async with async_session_maker() as session:

        try:
            details = await usecase.get_wallet_details(
                session,
                wallet_uuid,
                user
            )
        except wallet_exceptions.WalletNotFound:
            logger.warning("Wallet with id %s not found" % wallet_uuid)
            raise HTTPException(
                detail="Wallet with id: %s not found or it's not your wallet"
                % wallet_uuid,
                status_code=404
            )
        except wallet_exceptions.DetalizationError:
            logger.warning("Empty details list for wallet %s"
                           % wallet_uuid
                           )
            raise HTTPException(
                detail="Details for wallet %s is empty"
                       % wallet_uuid,
                status_code=400
            )
        except auth_exceptions.UserNotAuthorized:
            logger.warning("User not authorized for see wallet details")
            raise HTTPException(
                detail="You need authorize for see details",
                status_code=401
            )

        return {
            "message": "OK",
            "details": details,
        }
