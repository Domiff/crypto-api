from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models import Base


class CryptoCurrency(Base):
    __tablename__ = "crypto_currencies"

    ticker: Mapped[str] = mapped_column(index=True)
    index_price: Mapped[float]
    instrument_name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
