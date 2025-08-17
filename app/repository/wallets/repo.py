from app.repository.base import BaseRepo
from app.repository.wallets import models
from sqlalchemy import select


class WalletRepo(BaseRepo):
    model = models.Wallet

    @classmethod
    async def find_wallet_by_user(
            cls,
            user_id,
            session
    ):
        query = select(cls.model).where(
            cls.model.user_id == user_id
        )
        result = await session.execute(query)

        return result.scalars().first()


class WalletBalanceRepo(BaseRepo):
    model = models.WalletBalanceHistory

    @classmethod
    async def get_detalization(
            cls,
            session,
            wallet_id
    ):
        query = select(cls.model).where(
            cls.model.wallet_id == wallet_id,
        )
        result = await session.execute(query)

        return result.mappings().all()
