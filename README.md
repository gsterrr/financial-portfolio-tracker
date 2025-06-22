# Financial Portfolio Tracker

This is a simple web application for tracking the net worth of a financial portfolio. It is built with a Flask backend and a plain JavaScript and Bootstrap frontend.

## Features

- Track assets like stocks and properties.
- Automatically fetches current stock prices using the Finnhub API.
- Calculates portfolio performance, including total and annualized ROI.
- Supports multiple currencies with automatic exchange rate conversion.
- Allows for bulk import of assets via CSV upload.

## Project Structure

The application follows a service-oriented architecture to separate concerns:

```
/
├── .github/                # GitHub Actions workflows
│   └── workflows/
│       └── ci.yml          # Continuous Integration pipeline
├── app/                    # Main application folder
│   ├── __init__.py         # Application factory
│   ├── models.py           # SQLAlchemy database models
│   ├── routes/             # API and page routes
│   ├── services/           # Business logic layer
│   └── static/             # Frontend assets (JS, CSS)
├── tests/                  # Pytest test suite
│   └── test_app.py         # Application tests
├── venv/                   # Python virtual environment
├── .env                    # Environment variables (API keys)
├── app.py                  # Application entry point
├── requirements.txt        # Python dependencies
├── requirements-dev.txt    # Development dependencies
└── README.md               # This file
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    Install both production and development dependencies:
    ```bash
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    ```

4.  **Set up environment variables:**
    Create a file named `.env` in the root of the project and add your Finnhub API key:
    ```
    FINNHUB_API_KEY='YOUR_API_KEY_HERE'
    ```

## How to Run

1.  **Start the Flask application:**
    ```bash
    flask run
    ```

2.  Open your web browser and navigate to `http://127.0.0.1:5000`.

## Running Tests

The project includes a suite of tests using `pytest` to ensure everything is working correctly.

To run the tests, execute the following command from the root directory:
```bash
pytest
```

## Continuous Integration

This project uses GitHub Actions to automatically run tests and code analysis on every push and pull request to the `main` branch.

The CI pipeline performs the following checks:
-   **Code Formatting:** Ensures code style consistency using `black`.
-   **Linting:** Analyzes code for potential errors and style issues using `flake8`.
-   **Testing:** Runs the full `pytest` suite to verify application functionality.
    Create a file named `.env` in the root of the project and add your Finnhub API key:
    ```
    FINNHUB_API_KEY='YOUR_API_KEY_HERE'
    ```

## How to Run

1.  **Start the Flask application:**
    ```bash
    flask run
    ```

2.  Open your web browser and navigate to `http://127.0.0.1:5000`.

## Running Tests

The project includes a suite of tests using `pytest` to ensure everything is working correctly.

To run the tests, execute the following command from the root directory:
```bash
pytest
```


A comprehensive financial tracking application that helps you monitor your net worth across stocks, cryptocurrencies, and property investments.

## Features

- Track stock investments with real-time pricing
- Monitor cryptocurrency holdings
- Track property investments with rental income
- Calculate ROI (annualized)
- Track dividends and projected income
- Visualize portfolio performance
- Calculate net worth

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys (if needed):
```
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret
```

4. Run the application:
```bash
python app.py
```

The application will be available at http://localhost:5000

## API Endpoints

- GET `/api/assets` - Get all assets with current values and ROI
- GET `/api/properties` - Get all property investments
- GET `/api/net-worth` - Get total net worth calculation

## Development

The project is structured with:
- Flask backend for API endpoints
- SQLAlchemy for database management
- yfinance for stock data
- python-binance for cryptocurrency data
- SQLite database for local storage
