import io
import pandas as pd
from flask import Blueprint, jsonify, request
from ..models import db, Asset, Property, Dividend
from datetime import datetime
from ..services.finnhub_service import get_forex_rates, get_company_profile_and_quote
from ..services.portfolio_service import (
    process_asset_performance,
    calculate_annualized_roi,
)

main = Blueprint("main", __name__)


@main.route("/assets", methods=["GET"])
def get_assets():
    assets = Asset.query.all()
    result = []

    # Use the service to get FX rates
    fx_rates = get_forex_rates()

    for asset in assets:
        result.append(process_asset_performance(asset, fx_rates))
    return jsonify(result)


@main.route("/properties", methods=["GET"])
def get_properties():
    properties = Property.query.all()
    result = []
    for prop in properties:
        result.append(
            {
                "id": prop.id,
                "address": prop.address,
                "purchase_price": prop.purchase_price,
                "current_value": prop.current_value,
                "purchase_date": prop.purchase_date.isoformat(),
                "roi": calculate_annualized_roi(
                    prop.purchase_price, prop.current_value, prop.purchase_date
                ),
            }
        )
    return jsonify(result)


@main.route("/net-worth", methods=["GET"])
def get_net_worth():
    total_assets = sum(a.current_value for a in Asset.query.all())
    total_properties = sum(p.current_value for p in Property.query.all())
    return jsonify(
        {
            "total_assets": total_assets,
            "total_properties": total_properties,
            "net_worth": total_assets + total_properties,
        }
    )


@main.route("/upload/stocks", methods=["POST"])
def upload_stocks_csv():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected for uploading"}), 400

    if not file.filename.endswith(".csv"):
        return jsonify({"error": "Invalid file type. Please upload a .csv file."}), 400

    try:
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = pd.read_csv(stream)
        required_columns = ["ticker", "quantity", "purchase_date", "purchase_price"]
        if not all(col in csv_input.columns for col in required_columns):
            return jsonify({"error": f"CSV must have columns: {required_columns}"}), 400

        for _, row in csv_input.iterrows():
            ticker = row["ticker"]
            quantity = float(row["quantity"])
            purchase_date = datetime.strptime(row["purchase_date"], "%Y-%m-%d")
            purchase_price = float(row["purchase_price"])
            currency = row.get("currency", "USD").upper()
            purchase_fx_rate = float(row.get("purchase_fx_rate", 1.0))

            # Use the service to get company info and current price
            profile, quote = get_company_profile_and_quote(ticker)
            name = profile.get("name", ticker) if profile else ticker
            current_price = quote.get("c") or 0.0

            new_asset = Asset(
                type="stock",
                symbol=ticker,
                name=name,
                quantity=quantity,
                purchase_price=purchase_price,
                currency=currency,
                purchase_fx_rate=purchase_fx_rate,
                purchase_date=purchase_date,
                current_value=(current_price * quantity),
            )
            db.session.add(new_asset)

        db.session.commit()
        return (
            jsonify({"message": f"{len(csv_input)} assets processed successfully."}),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
