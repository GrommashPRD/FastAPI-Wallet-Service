from app.auth.dependencies import CurrentUserDep
from app.repository.wallets import repo
from sqlalchemy.ext.asyncio import AsyncSession
from app.usecase.wallets import exceptions as wallet_exceptions
from app.usecase.auth import exceptions as auth_exceptions
from app.api.handlers.wallets import schemas as wallet_schemas
from decimal import Decimal


async def deposit(
        session,
        wallet_uuid,
        amount
):
    wallet = await repo.WalletRepo.find_by_id(id=wallet_uuid)
    if not wallet:
        raise wallet_exceptions.WalletNotFound(
            detail="Wallet with ID: %s, not found."
        )

    new_balance = wallet.balance + amount

    detail = await repo.WalletBalanceRepo.add_new(
        session,
        wallet_id=wallet_uuid,
        old_balance=wallet.balance,
        operation=wallet_schemas.SOperation.DEPOSIT,
        amount=amount,
        new_balance=new_balance
    )

    wallet.balance = new_balance
    session.add_all([wallet, detail])
    await session.commit()


async def withdraw(
        session: AsyncSession,
        user,
        wallet_uuid: str,
        amount: Decimal
):
    wallet = await repo.WalletRepo.find_wallet_by_user(
        user.id,
        session
    )

    if not wallet or wallet.id != wallet_uuid:
        raise wallet_exceptions.WalletNotFound(
            detail="Wallet with ID: %s, \
            not found or it's not your wallet"
            % wallet_uuid
        )

    if amount > wallet.balance:
        raise wallet_exceptions.InsufficientFunds(
            detail="Insufficient funds for withdrawal"
        )

    new_balance = wallet.balance - amount

    detail = await repo.WalletBalanceRepo.add_new(
        session,
        wallet_id=wallet_uuid,
        old_balance=wallet.balance,
        operation=wallet_schemas.SOperation.DEPOSIT,
        amount=amount,
        new_balance=new_balance
    )

    wallet.balance = new_balance
    session.add_all([wallet, detail])
    await session.commit()


async def update_wallet_balance(
        session: AsyncSession,
        wallet_uuid: str,
        request,
        user=CurrentUserDep
):
    if request.operation == wallet_schemas.SOperation.DEPOSIT:
        try:
            await deposit(
                session,
                wallet_uuid,
                request.amount
            )
        except wallet_exceptions.WalletNotFound:
            raise wallet_exceptions.WalletNotFound(
                detail="Wallet with id: %s not found"
                       % wallet_uuid
            )

    if request.operation == wallet_schemas.SOperation.WITHDRAW:
        if not user:
            raise auth_exceptions.UserNotAuthorized(
                detail="User must be authenticated to withdraw."
            )
        try:
            await withdraw(
                session,
                user,
                wallet_uuid,
                request.amount,
            )
        except wallet_exceptions.InsufficientFunds:
            raise wallet_exceptions.InsufficientFunds(
                detail="Insufficient funds in the balance"
            )
        except wallet_exceptions.WalletNotFound:
            raise wallet_exceptions.WalletNotFound(
                detail="Wallet with id: %s not found"
                       % wallet_uuid
            )
