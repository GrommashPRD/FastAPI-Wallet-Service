from sqlalchemy import Column, String, ForeignKey, Integer, Numeric, Enum
from decimal import Decimal
from sqlalchemy.orm import relationship
from app.database import Base
import enum
import uuid

class Operations(enum.Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    balance = Column(
        Numeric(
            18,
            8),
        nullable=False,
        default=Decimal('0')
    )
    user_id = Column(
        String,
        ForeignKey('users.id'),
        nullable=False,
        unique=True
    )

    owner = relationship("User", back_populates="wallet")
    balance_history = relationship("WalletBalanceHistory", back_populates="wallet")


class WalletBalanceHistory(Base):
    __tablename__ = "balance detalization"

    id = Column(String, primary_key=True,
                default=lambda: str(uuid.uuid4()), unique=True
                )
    wallet_id = Column(String, ForeignKey('wallets.id'), nullable=False)
    old_balance = Column(Numeric(18, 8), nullable=False)
    operation = Column(Enum(Operations), nullable=False)
    amount = Column(Integer, nullable=False)
    new_balance = Column(Numeric(18, 8), nullable=False)

    wallet = relationship("Wallet", back_populates="balance_history")
