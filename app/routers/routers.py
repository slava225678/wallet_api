from fastapi import APIRouter

from .endpoints.wallet import router as wallet_router

main_router = APIRouter()
main_router.include_router(
    wallet_router,
    prefix="/api/v1/wallets",
    tags=["Wallets"]
)
