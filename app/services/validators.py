from decimal import Decimal

from fastapi import HTTPException, status

from app.constants import ERR_INSUFFICIENT_FUNDS
from app.models.wallet import Wallet


def check_sufficient_funds(wallet: Wallet, amount: Decimal) -> None:
    """Проверяет, достаточно ли средств на счёте."""
    if wallet.balance < amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERR_INSUFFICIENT_FUNDS
        )
