from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import ERR_WALLET_NOT_FOUND
from app.models.wallet import Wallet


async def get_wallet_by_id(
    wallet_id: UUID,
    session: AsyncSession,
    for_update: bool = False
) -> Wallet:
    """
    Получить объект кошелька по его UUID.

    Если `for_update=True`, выполняется блокировка строки (SELECT FOR UPDATE),
    чтобы избежать состояния гонки при обновлении баланса.

    Args:
        wallet_id (UUID): Идентификатор кошелька.
        session (AsyncSession): Асинхронная сессия базы данных.
        for_update (bool, optional):
        Применить SELECT FOR UPDATE. По умолчанию False.

    Returns:
        Wallet: Объект кошелька из базы данных.

    Raises:
        HTTPException: 404, если кошелёк не найден.
    """
    stmt = select(Wallet).where(Wallet.id == wallet_id)
    if for_update:
        stmt = stmt.with_for_update()

    result = await session.execute(stmt)
    wallet = result.scalar_one_or_none()

    if wallet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERR_WALLET_NOT_FOUND
        )

    return wallet
