import uuid

from sqlalchemy import Column, Numeric
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    balance = Column(
        Numeric(precision=10, scale=2),
        nullable=False,
        default=0
    )
