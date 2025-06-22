from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    symbol = db.Column(db.String(20), nullable=True, unique=True)
    quantity = db.Column(db.Float, nullable=True)
    purchase_price = db.Column(db.Float, nullable=True)
    currency = db.Column(db.String(10), nullable=False, default="USD")
    purchase_fx_rate = db.Column(db.Float, nullable=False, default=1.0)
    current_value = db.Column(db.Float, nullable=True)
    purchase_date = db.Column(db.DateTime, nullable=True)
    dividends = db.relationship("Dividend", backref="asset", lazy=True)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey("asset.id"), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # e.g., 'buy', 'sell'
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)


class Dividend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey("asset.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    projected = db.Column(db.Boolean, default=False)


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    current_value = db.Column(db.Float)
    purchase_date = db.Column(db.DateTime, nullable=False)
    rental_income = db.Column(db.Float)
    expenses = db.Column(db.Float)


class ApiCache(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), nullable=False, unique=True)
    data = db.Column(db.JSON, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
