from datetime import datetime
from ..services.finnhub_service import get_stock_data

def calculate_total_roi(purchase_price, current_value):
    if purchase_price == 0:
        return 0
    return ((current_value / purchase_price) - 1) * 100

def calculate_annualized_roi(purchase_price, current_value, purchase_date):
    if purchase_price == 0:
        return 0
    days_held = (datetime.now() - purchase_date).days
    if days_held < 1:
        return calculate_total_roi(purchase_price, current_value) # Not held long enough for annualization
    
    annualized_return = (current_value / purchase_price) ** (365.0 / days_held) - 1
    return annualized_return * 100

def process_asset_performance(asset, fx_rates):
    """Calculates performance metrics for a single asset."""
    current_price = 0
    asset_growth_usd = 0
    currency_gain_usd = 0
    dividend_income_usd = 0

    if asset.type.lower() == 'stock':
        try:
            profile, quote = get_stock_data(asset.symbol)
            current_price = quote.get('c') or 0.0
            quantity = asset.quantity or 0.0
            asset.current_value = current_price * quantity

            if asset.purchase_price is not None and asset.purchase_price > 0 and fx_rates:
                current_fx_rate = fx_rates.get(asset.currency, 1.0) if asset.currency != 'USD' else 1.0

                asset_growth_local = (current_price - asset.purchase_price) * quantity
                asset_growth_usd = asset_growth_local * current_fx_rate

                currency_gain_usd = (current_fx_rate - (asset.purchase_fx_rate or 1.0)) * quantity * asset.purchase_price

                dividend_income_usd = sum(d.amount for d in asset.dividends) * current_fx_rate

        except Exception as e:
            print(f"Could not process stock {asset.symbol}: {e}")

    total_gain_usd = asset_growth_usd + currency_gain_usd + dividend_income_usd

    return {
        'id': asset.id,
        'type': asset.type,
        'symbol': asset.symbol,
        'name': asset.name,
        'quantity': asset.quantity,
        'purchase_price': asset.purchase_price,
        'purchase_date': asset.purchase_date.strftime('%Y-%m-%d') if asset.purchase_date else None,
        'currency': asset.currency,
        'current_price': current_price,
        'current_value': asset.current_value,
        'asset_growth_usd': asset_growth_usd,
        'currency_gain_usd': currency_gain_usd,
        'dividend_income_usd': dividend_income_usd,
        'total_gain': total_gain_usd,
        'dividends': [{'amount': d.amount, 'date': d.date.isoformat(), 'projected': d.projected} for d in asset.dividends]
    }
