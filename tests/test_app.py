import pytest
import json
from datetime import date
from app import create_app, db
from app.models import Asset

# Mock data to be returned by the Finnhub API during tests
MOCK_QUOTE = {
    "c": 150.0,
    "d": -2.5,
    "dp": -1.64,
    "h": 155.0,
    "l": 149.0,
    "o": 152.0,
    "pc": 152.5,
}
MOCK_PROFILE = {"name": "Apple Inc.", "logo": "some_url"}
MOCK_FOREX = {"base": "EUR", "quote": {"USD": 1.1}}


@pytest.fixture
def client():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config["TESTING"] = True
    # Use an in-memory SQLite database for tests to avoid interfering with your real data
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.drop_all()  # Ensure a clean slate
        db.create_all()
        # Add a sample asset to the test database
        test_asset = Asset(
            symbol="AAPL",
            name="Apple Inc.",
            type="Stock",
            quantity=10,
            purchase_price=100.0,
            purchase_date=date(2022, 1, 1),
            currency="USD",
        )
        db.session.add(test_asset)
        db.session.commit()

        with app.test_client() as client:
            yield client


def test_home_page(client):
    """Test that the home page loads correctly."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"<title>Financial Tracker</title>" in response.data


def test_assets_page_loads(client):
    """Test that the assets page loads correctly."""
    response = client.get("/assets")
    assert response.status_code == 200
    assert b"<h2>Assets</h2>" in response.data


def test_api_assets(client, mocker):
    """Test the /api/assets endpoint with mocked Finnhub data."""
    # Mock the Finnhub API client methods at their new location in the service layer
    mocker.patch(
        "app.services.finnhub_service.finnhub_client.quote", return_value=MOCK_QUOTE
    )
    mocker.patch(
        "app.services.finnhub_service.finnhub_client.company_profile2",
        return_value=MOCK_PROFILE,
    )
    mocker.patch(
        "app.services.finnhub_service.finnhub_client.forex_rates",
        return_value=MOCK_FOREX,
    )

    # Make a request to the API endpoint
    response = client.get("/api/assets")
    assert response.status_code == 200

    # Parse the JSON response and verify its contents
    data = json.loads(response.data)
    assert len(data) == 1
    asset_data = data[0]

    assert asset_data["symbol"] == "AAPL"
    assert asset_data["name"] == "Apple Inc."
    assert asset_data["current_price"] == 150.0
    assert asset_data["purchase_date"] == "2022-01-01"

    # Verify the backend calculation is correct
    # Initial value = 10 * 100 = 1000
    # Current value = 10 * 150 = 1500
    # Total Gain = 1500 - 1000 = 500
    assert asset_data["total_gain"] == 500.0
