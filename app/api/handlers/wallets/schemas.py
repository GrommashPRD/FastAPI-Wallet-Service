from pydantic import BaseModel
from decimal import Decimal
from enum import Enum


class SDepositRequest(BaseModel):
    wallet_id: int
    amount: Decimal


class SOperation(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class SOperationRequest(BaseModel):
    operation: SOperation
    amount: Decimal
