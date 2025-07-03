from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import ERR_INVALID_OPERATION_TYPE
from app.core.database import get_db
from app.schemas.wallet import OperationType, WalletBalance, WalletOperation
from app.services.validators import check_sufficient_funds
from app.services.wallet import get_wallet_by_id

router = APIRouter()


@router.get("/{wallet_uuid}", response_model=WalletBalance)
async def get_wallet_balance(
    wallet_uuid: UUID,
    session: AsyncSession = Depends(get_db)
) -> WalletBalance:
    """
    Получить текущий баланс указанного кошелька.

    Args:
        wallet_uuid (UUID): Уникальный идентификатор кошелька.
        session (AsyncSession): Асинхронная сессия базы данных.

    Returns:
        WalletBalance: Объект с информацией о балансе кошелька.

    Raises:
        HTTPException: 404, если кошелёк не найден.
    """
    wallet = await get_wallet_by_id(wallet_uuid, session)
    return WalletBalance(wallet_uuid=wallet.id, balance=wallet.balance)


@router.post("/{wallet_uuid}/operation", response_model=WalletBalance)
async def perform_wallet_operation(
    wallet_uuid: UUID,
    operation: WalletOperation,
    session: AsyncSession = Depends(get_db)
) -> WalletBalance:
    """
    Выполнить операцию с балансом кошелька (пополнение или списание).

    Использует блокировку строки в базе данных (SELECT FOR UPDATE) для 
    безопасной работы в конкурентной среде.

    Args:
        wallet_uuid (UUID): Уникальный идентификатор кошелька.
        operation (WalletOperation): Операция пополнения или списания.
        session (AsyncSession): Асинхронная сессия базы данных.

    Returns:
        WalletBalance: Обновлённое состояние баланса кошелька.

    Raises:
        HTTPException: 400, если тип операции недопустим.
        HTTPException: 404, если кошелёк не найден.
        HTTPException: 400, если недостаточно средств при списании.
    """
    async with session.begin():
        wallet = await get_wallet_by_id(wallet_uuid, session, for_update=True)

        if operation.operation_type == OperationType.deposit:
            wallet.balance += operation.amount
        elif operation.operation_type == OperationType.withdraw:
            check_sufficient_funds(wallet, operation.amount)
            wallet.balance -= operation.amount
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERR_INVALID_OPERATION_TYPE
            )

        session.add(wallet)

    return WalletBalance(wallet_uuid=wallet.id, balance=wallet.balance)
