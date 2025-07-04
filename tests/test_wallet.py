from uuid import uuid4

import pytest
from fastapi import status
from httpx import AsyncClient

from app.constants import (BASE_URL, ERR_INSUFFICIENT_FUNDS, FIFTEEN, NULL,
                           ONE_HUN, TWO_HUN)
from app.models import Wallet
from app.schemas.wallet import OperationType


@pytest.mark.asyncio
async def test_wallet_deposit_and_balance(session, client: AsyncClient):
    """
    Проверяет успешное пополнение 
    кошелька и получение актуального баланса.
    """
    wallet = Wallet(id=uuid4(), balance=NULL)
    session.add(wallet)
    await session.commit()

    response = await client.post(
        f"{BASE_URL}/{wallet.id}/operation",
        json={"operation_type": OperationType.deposit, "amount": ONE_HUN}
    )
    assert response.status_code == TWO_HUN
    data = response.json()
    assert data["balance"] == ONE_HUN

    response = await client.get(f"{BASE_URL}/{wallet.id}")
    assert response.status_code == TWO_HUN
    assert response.json()["balance"] == ONE_HUN


@pytest.mark.asyncio
async def test_wallet_withdraw_insufficient_funds(
    """Проверяет отказ операции снятия при недостаточном балансе."""
    session, client:
    AsyncClient
):
    wallet = Wallet(id=uuid4(), balance=10)
    session.add(wallet)
    await session.commit()

    response = await client.post(
        f"{BASE_URL}/{wallet.id}/operation",
        json={"operation_type": OperationType.withdraw, "amount": FIFTEEN}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == ERR_INSUFFICIENT_FUNDS


@pytest.mark.asyncio
async def test_wallet_invalid_uuid(client: AsyncClient):
    """Проверяет, что при некорректном UUID вернётся 422 ошибка валидации."""
    invalid_uuid = "not-a-uuid"
    response = await client.get(f"{BASE_URL}/{invalid_uuid}")
    assert (response.status_code
            == status.HTTP_422_UNPROCESSABLE_ENTITY
            )  # FastAPI валидирует uuid автоматом


@pytest.mark.asyncio
async def test_wallet_invalid_operation_type(session, client: AsyncClient):
    """Проверяет, что FastAPI отклонит запрос с недопустимым типом операции."""
    wallet = Wallet(id=uuid4(), balance=ONE_HUN)
    session.add(wallet)
    await session.commit()

    response = await client.post(
        f"{BASE_URL}/{wallet.id}/operation",
        json={"operation_type": "invalid", "amount": 50}
    )
    assert (response.status_code
            == status.HTTP_422_UNPROCESSABLE_ENTITY
            )  # FastAPI выбросит ошибку валидации
