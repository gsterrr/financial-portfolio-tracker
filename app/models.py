from datetime import datetime
from typing import List, Optional

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Asset(Base):
    __tablename__ = "asset"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(50))
    name: Mapped[str] = mapped_column(String(100))
    symbol: Mapped[Optional[str]] = mapped_column(String(20), unique=True)
    quantity: Mapped[Optional[float]] = mapped_column()
    purchase_price: Mapped[Optional[float]] = mapped_column()
    currency: Mapped[str] = mapped_column(String(10), default="USD")
    purchase_fx_rate: Mapped[float] = mapped_column(default=1.0)
    current_value: Mapped[Optional[float]] = mapped_column()
    purchase_date: Mapped[Optional[datetime]] = mapped_column()
    dividends: Mapped[List["Dividend"]] = relationship(backref="asset", lazy=True)


class Transaction(Base):
    __tablename__ = "transaction"
    id: Mapped[int] = mapped_column(primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("asset.id"))
    type: Mapped[str] = mapped_column(String(50))  # e.g., 'buy', 'sell'
    quantity: Mapped[float] = mapped_column()
    price: Mapped[float] = mapped_column()
    date: Mapped[datetime] = mapped_column()


class Dividend(Base):
    __tablename__ = "dividend"
    id: Mapped[int] = mapped_column(primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("asset.id"))
    amount: Mapped[float] = mapped_column()
    date: Mapped[datetime] = mapped_column()
    projected: Mapped[bool] = mapped_column(default=False)


class Property(Base):
    __tablename__ = "property"
    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(200))
    purchase_price: Mapped[float] = mapped_column()
    current_value: Mapped[Optional[float]] = mapped_column()
    purchase_date: Mapped[Optional[datetime]] = mapped_column()
    rental_income: Mapped[Optional[float]] = mapped_column()
    expenses: Mapped[Optional[float]] = mapped_column()


class ApiCache(Base):
    __tablename__ = "api_cache"
    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String(20), unique=True)
    data: Mapped[dict] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)
