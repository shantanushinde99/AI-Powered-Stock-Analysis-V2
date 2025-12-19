"""
Unified data vendor interface for fetching stock data from multiple sources.
Supports Yahoo Finance (yfinance) and Alpha Vantage.
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
from typing import Optional, Tuple


def get_data_vendor_selection() -> Tuple[str, Optional[str]]:
    """
    Display data vendor selection UI in sidebar and return selection.
    
    Returns:
        Tuple of (vendor_name, api_key)
        - vendor_name: "yfinance" or "alpha_vantage"
        - api_key: API key if Alpha Vantage selected, None otherwise
    """
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Data Source")
    
    vendor = st.sidebar.radio(
        "Select Data Vendor",
        options=["Yahoo Finance", "Alpha Vantage"],
        help="Yahoo Finance is free (no API key needed). Alpha Vantage requires API key but offers more detailed data."
    )
    
    api_key = None
    
    if vendor == "Alpha Vantage":
        api_key = st.sidebar.text_input(
            "Alpha Vantage API Key",
            type="password",
            value=os.getenv("ALPHA_VANTAGE_API_KEY", ""),
            help="Get your free API key from https://www.alphavantage.co/support/#api-key"
        )
        
        if api_key:
            os.environ["ALPHA_VANTAGE_API_KEY"] = api_key
            st.sidebar.success("✅ API key set")
        else:
            st.sidebar.warning("⚠️ API key required")
    else:
        st.sidebar.info("ℹ️ No API key needed")
    
    vendor_name = "alpha_vantage" if vendor == "Alpha Vantage" else "yfinance"
    return vendor_name, api_key


def fetch_stock_data(
    ticker: str,
    start_date: datetime,
    end_date: datetime,
    vendor: str = "yfinance",
    api_key: Optional[str] = None,
    interval: str = "1d"
) -> Optional[pd.DataFrame]:
    """
    Fetch stock data from the specified vendor.
    
    Args:
        ticker: Stock symbol (e.g., "AAPL")
        start_date: Start date for data
        end_date: End date for data
        vendor: "yfinance" or "alpha_vantage"
        api_key: Alpha Vantage API key (required if vendor is alpha_vantage)
        interval: Data interval (e.g., "1d", "1h") - only used for yfinance
        
    Returns:
        DataFrame with columns: Open, High, Low, Close, Volume
        Index: DatetimeIndex with timezone
    """
    
    if vendor == "yfinance":
        return _fetch_from_yfinance(ticker, start_date, end_date, interval)
    elif vendor == "alpha_vantage":
        if not api_key:
            st.error("❌ Alpha Vantage API key is required")
            return None
        return _fetch_from_alpha_vantage(ticker, start_date, end_date, api_key)
    else:
        st.error(f"❌ Unsupported vendor: {vendor}")
        return None


def _fetch_from_yfinance(
    ticker: str,
    start_date: datetime,
    end_date: datetime,
    interval: str = "1d"
) -> Optional[pd.DataFrame]:
    """Fetch data from Yahoo Finance using yfinance."""
    try:
        import yfinance as yf
        
        df = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            interval=interval,
            progress=False
        )
        
        if df.empty:
            st.error(f"No data found for {ticker}")
            return None
        
        # Handle MultiIndex columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        
        # Ensure we have the required columns
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        df = df[required_cols]
        df = df.dropna()
        df.index.name = 'Date'
        
        # Ensure UTC timezone
        if df.index.tz is None:
            df.index = pd.to_datetime(df.index, utc=True)
        
        return df
        
    except ImportError:
        st.error("❌ yfinance library not installed. Run: pip install yfinance")
        return None
    except Exception as e:
        st.error(f"❌ Error fetching data from Yahoo Finance: {e}")
        return None


def _fetch_from_alpha_vantage(
    ticker: str,
    start_date: datetime,
    end_date: datetime,
    api_key: str
) -> Optional[pd.DataFrame]:
    """Fetch data from Alpha Vantage."""
    try:
        import requests
        
        # Alpha Vantage API endpoint for daily data
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": ticker,
            "apikey": api_key,
            "outputsize": "full"  # Get full historical data
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        # Check for various error/info messages
        if "Error Message" in data:
            st.error(f"❌ Alpha Vantage Error: {data['Error Message']}")
            return None
        
        if "Note" in data:
            st.error(f"⚠️ Alpha Vantage Rate Limit: {data['Note']}")
            st.info("💡 Switch to Yahoo Finance or wait a moment before trying again.")
            return None
        
        if "Information" in data:
            st.error(f"⚠️ Alpha Vantage API Limit: {data['Information']}")
            st.info("💡 You may have exceeded your API quota. Free tier allows 25 requests/day.")
            st.info("🔄 Tip: Switch to Yahoo Finance in the data source dropdown for unlimited access.")
            return None
        
        if "Time Series (Daily)" not in data:
            st.error(f"❌ Unexpected response from Alpha Vantage")
            st.warning(f"Response keys: {list(data.keys())}")
            st.info("💡 Try using Yahoo Finance instead.")
            return None
        
        # Parse the time series data
        time_series = data["Time Series (Daily)"]
        
        # Convert to DataFrame
        df = pd.DataFrame.from_dict(time_series, orient='index')
        df.index = pd.to_datetime(df.index)
        df.index.name = 'Date'
        
        # Rename columns to match yfinance format
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        
        # Convert to numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Filter by date range
        df = df.sort_index()
        df = df.loc[start_date:end_date]
        
        # Ensure UTC timezone
        df.index = pd.to_datetime(df.index, utc=True)
        
        if df.empty:
            st.error(f"No data found for {ticker} in the specified date range")
            return None
        
        return df
        
    except ImportError:
        st.error("❌ requests library not installed. Run: pip install requests")
        return None
    except Exception as e:
        st.error(f"❌ Error fetching data from Alpha Vantage: {e}")
        return None


def get_current_price(ticker: str, vendor: str = "yfinance", api_key: Optional[str] = None) -> float:
    """
    Get the current/latest price for a ticker.
    
    Args:
        ticker: Stock symbol
        vendor: "yfinance" or "alpha_vantage"
        api_key: Alpha Vantage API key (if using alpha_vantage)
        
    Returns:
        Current price as float, or 0.0 if unavailable
    """
    try:
        from datetime import timedelta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=5)  # Get last 5 days
        
        df = fetch_stock_data(ticker, start_date, end_date, vendor, api_key)
        
        if df is not None and not df.empty:
            return float(df['Close'].iloc[-1])
        
    except Exception as e:
        st.warning(f"⚠️ Could not fetch current price: {e}")
    
    return 0.0
