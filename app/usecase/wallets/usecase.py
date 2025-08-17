from app.repository.wallets import repo
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.handlers.auth import schemas
from app.repository import exceptions as repository_exceptions
from app.usecase.wallets import exceptions as wallet_exceptions
from app.usecase.auth import exceptions as auth_exceptions


async def create_new_wallet(
        user: schemas.SUser,
        session: AsyncSession
):
    if not user:
        raise auth_exceptions.UserNotAuthorized(
            detail="User must be authenticated to see details."
        )
    try:
        wallet = await repo.WalletRepo.add_new(
            session,
            check_conditions={"user_id": user.id},
            user_id=user.id
        )

    except repository_exceptions.RecordAlreadyExist:
        raise wallet_exceptions.UserAlreadyHaveWallet(
            detail="User %s already have wallet"
        )

    session.add(wallet)
    await session.commit()

    return wallet


async def get_user_wallet(
        session: AsyncSession,
        user: schemas.SUser,
        wallet_uuid: str = None,
):
    if not user:
        raise auth_exceptions.UserNotAuthorized(
            detail="User must be authenticated to see a balance."
        )

    wallet = await repo.WalletRepo.find_wallet_by_user(
        user_id=user.id,
        session=session
    )

    if not wallet:
        raise wallet_exceptions.WalletDontExist(
            detail="User dont have a wallet"
        )

    if wallet_uuid and wallet.id != wallet_uuid:
        raise wallet_exceptions.WalletNotFound(
            detail="Wallet with id: %s not found or it's not your wallet"
                   % wallet_uuid
        )

    return wallet


async def get_wallet_details(
        session: AsyncSession,
        wallet_uuid: str,
        user: schemas.SUser
):
    if not user:
        raise auth_exceptions.UserNotAuthorized(
            detail="User must be authenticated to see details."
        )

    wallet = await repo.WalletRepo.find_wallet_by_user(
        user.id,
        session
    )

    if not wallet or wallet.id != wallet_uuid:
        raise wallet_exceptions.WalletNotFound(
            detail="Wallet with id: %s not found or it's not your wallet"
                   % wallet_uuid
        )

    details = await repo.WalletBalanceRepo.get_detalization(
        session,
        wallet.id
    )
    if not details:
        raise wallet_exceptions.DetalizationError(detail="Details is empty")

    return details
