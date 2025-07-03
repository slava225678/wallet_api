from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from app.constants import MIN_OPERATION_AMOUNT


class OperationType(str, Enum):
    """Тип операции с кошельком."""
    deposit = "DEPOSIT"
    withdraw = "WITHDRAW"


class WalletOperation(BaseModel):
    """
    Входная модель операции с кошельком:
    пополнение или списание.
    """
    operation_type: OperationType
    amount: Decimal = Field(..., gt=0)

    @field_validator("amount")
    def validate_amount_positive(cls, value: Decimal) -> Decimal:
        """Проверяет, что сумма операции больше минимального значения."""
        if value < MIN_OPERATION_AMOUNT:
            raise ValueError(
                f"The transaction amount must be at least {
                    MIN_OPERATION_AMOUNT
                }"
            )
        return value


class WalletBalance(BaseModel):
    """Выходная модель с текущим балансом кошелька."""
    wallet_uuid: UUID
    balance: Decimal

    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }
