import os
import finnhub
from datetime import datetime, timedelta
from ..models import db, ApiCache

# Initialize Finnhub client
finnhub_client = finnhub.Client(api_key=os.environ.get('FINNHUB_API_KEY'))

def get_stock_data(symbol):
    """
    Fetches stock profile and quote from Finnhub API, using a cache.
    Returns a tuple of (profile, quote).
    """
    cache_entry = ApiCache.query.filter_by(symbol=symbol).first()

    if cache_entry and (datetime.now() - cache_entry.timestamp) < timedelta(minutes=15):
        return cache_entry.data.get('profile', {}), cache_entry.data.get('quote', {})

    # Fetch new data and update cache
    profile, quote = {}, {}
    try:
        print(f"DEBUG: Attempting to fetch company_profile2 for {symbol}.")
        profile = finnhub_client.company_profile2(symbol=symbol)
        print(f"DEBUG: Successfully fetched company_profile2 for {symbol}.")
    except Exception as e:
        print(f"ERROR: Failed to fetch company_profile2 for {symbol}. Error: {e}")

    try:
        print(f"DEBUG: Attempting to fetch quote for {symbol}.")
        quote = finnhub_client.quote(symbol)
        print(f"DEBUG: Successfully fetched quote for {symbol}.")
    except Exception as e:
        print(f"ERROR: Failed to fetch quote for {symbol}. Error: {e}")

    new_data = {'profile': profile, 'quote': quote}

    if cache_entry:
        cache_entry.data = new_data
        cache_entry.timestamp = datetime.now()
    else:
        new_cache_entry = ApiCache(symbol=symbol, data=new_data, timestamp=datetime.now())
        db.session.add(new_cache_entry)
    db.session.commit()

    return profile, quote

def get_forex_rates():
    """
    Fetches forex rates from Finnhub API, using a cache.
    Returns a dictionary of forex rates.
    """
    fx_cache = ApiCache.query.filter_by(symbol='FX_RATES').first()
    if fx_cache and (datetime.now() - fx_cache.timestamp) < timedelta(minutes=60):
        return fx_cache.data

    try:
        print("DEBUG: Attempting to fetch forex_rates from Finnhub.")
        api_fx_rates = finnhub_client.forex_rates(base='USD')
        if api_fx_rates and 'quote' in api_fx_rates:
            fx_rates = api_fx_rates['quote']
            if fx_cache:
                fx_cache.data = fx_rates
                fx_cache.timestamp = datetime.now()
            else:
                db.session.add(ApiCache(symbol='FX_RATES', data=fx_rates, timestamp=datetime.now()))
            db.session.commit()
            print("DEBUG: Successfully fetched and cached forex_rates.")
            return fx_rates
    except Exception as e:
        print(f"ERROR: Failed to fetch forex_rates. Error: {e}")
    
    return None
