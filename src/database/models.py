from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)
    index_price: Mapped[float]
    instrument_name: Mapped[str]
    timestamp: Mapped[int]


class Btc(Base):
    pass


class Eth(Base):
    pass
