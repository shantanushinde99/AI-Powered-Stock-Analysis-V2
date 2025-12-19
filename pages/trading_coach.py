"""
Trading Coach - Real-time Price Fetcher
Fetches current prices for stocks and cryptocurrencies using Finnhub and FCS APIs.

Sample assets:
- Stocks: Apple (AAPL), Microsoft (MSFT), Tesla (TSLA), etc.
- Cryptos: Bitcoin (BTC), Ethereum (ETH), Solana (SOL), etc.
"""

import os
import requests
import streamlit as st
from datetime import datetime
import pandas as pd
import time

# API Configuration
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY', '')
FCS_API_KEY = os.getenv('FCS_API_KEY', '')

# API Base URLs
FINNHUB_BASE_URL = "https://finnhub.io/api/v1"
FCS_BASE_URL = "https://fcsapi.com/api-v3"

# ==========================================
# AVAILABLE ASSETS IN FREE API TIERS
# ==========================================

# Popular US Stocks (Available in Finnhub Free Tier)
AVAILABLE_STOCKS = {
    # Technology
    'AAPL': 'Apple Inc.',
    'MSFT': 'Microsoft Corporation',
    'GOOGL': 'Alphabet Inc. (Google)',
    'AMZN': 'Amazon.com Inc.',
    'META': 'Meta Platforms Inc. (Facebook)',
    'NVDA': 'NVIDIA Corporation',
    'TSLA': 'Tesla Inc.',
    'AMD': 'Advanced Micro Devices',
    'INTC': 'Intel Corporation',
    'CRM': 'Salesforce Inc.',
    'ORCL': 'Oracle Corporation',
    'ADBE': 'Adobe Inc.',
    'NFLX': 'Netflix Inc.',
    'PYPL': 'PayPal Holdings',
    'UBER': 'Uber Technologies',
    
    # Finance
    'JPM': 'JPMorgan Chase & Co.',
    'BAC': 'Bank of America Corp.',
    'WFC': 'Wells Fargo & Company',
    'GS': 'Goldman Sachs Group',
    'MS': 'Morgan Stanley',
    'V': 'Visa Inc.',
    'MA': 'Mastercard Inc.',
    
    # Healthcare
    'JNJ': 'Johnson & Johnson',
    'PFE': 'Pfizer Inc.',
    'UNH': 'UnitedHealth Group',
    'MRNA': 'Moderna Inc.',
    'ABBV': 'AbbVie Inc.',
    
    # Consumer
    'WMT': 'Walmart Inc.',
    'KO': 'Coca-Cola Company',
    'PEP': 'PepsiCo Inc.',
    'MCD': 'McDonald\'s Corporation',
    'NKE': 'Nike Inc.',
    'SBUX': 'Starbucks Corporation',
    'DIS': 'Walt Disney Company',
    
    # Energy
    'XOM': 'Exxon Mobil Corporation',
    'CVX': 'Chevron Corporation',
    
    # Industrial
    'BA': 'Boeing Company',
    'CAT': 'Caterpillar Inc.',
    'GE': 'General Electric',
    
    # ETFs & Indices
    'SPY': 'SPDR S&P 500 ETF',
    'QQQ': 'Invesco QQQ Trust (Nasdaq)',
    'DIA': 'SPDR Dow Jones ETF',
    'IWM': 'iShares Russell 2000 ETF',
    'VTI': 'Vanguard Total Stock Market ETF',
}

# Popular Cryptocurrencies (Available in Free Tier)
AVAILABLE_CRYPTOS = {
    'BTC': 'Bitcoin',
    'ETH': 'Ethereum',
    'BNB': 'Binance Coin',
    'XRP': 'Ripple',
    'ADA': 'Cardano',
    'SOL': 'Solana',
    'DOGE': 'Dogecoin',
    'DOT': 'Polkadot',
    'MATIC': 'Polygon',
    'SHIB': 'Shiba Inu',
    'LTC': 'Litecoin',
    'AVAX': 'Avalanche',
    'LINK': 'Chainlink',
    'UNI': 'Uniswap',
    'ATOM': 'Cosmos',
    'XLM': 'Stellar',
    'ETC': 'Ethereum Classic',
    'FIL': 'Filecoin',
    'NEAR': 'NEAR Protocol',
    'APE': 'ApeCoin',
    'ALGO': 'Algorand',
    'VET': 'VeChain',
    'MANA': 'Decentraland',
    'SAND': 'The Sandbox',
    'AXS': 'Axie Infinity',
    'TRX': 'TRON',
    'AAVE': 'Aave',
    'MKR': 'Maker',
    'COMP': 'Compound',
}

# Available Timeframes
AVAILABLE_TIMEFRAMES = {
    '1': '1 Minute',
    '5': '5 Minutes',
    '15': '15 Minutes',
    '60': '1 Hour',
    'D': 'Daily',
}


class TradingCoach:
    """Trading Coach class for fetching real-time prices from multiple APIs"""
    
    def __init__(self, finnhub_key=None, fcs_key=None):
        """
        Initialize the Trading Coach with API keys
        
        Args:
            finnhub_key (str): Finnhub API key
            fcs_key (str): FCS API key
        """
        self.finnhub_key = finnhub_key or FINNHUB_API_KEY
        self.fcs_key = fcs_key or FCS_API_KEY
        
    def get_stock_price_finnhub(self, symbol):
        """
        Fetch current stock price from Finnhub API
        
        Args:
            symbol (str): Stock symbol (e.g., 'AAPL', 'MSFT')
            
        Returns:
            dict: Stock price data including current, high, low, open, previous close
        """
        if not self.finnhub_key:
            return {"error": "Finnhub API key not configured"}
        
        url = f"{FINNHUB_BASE_URL}/quote"
        params = {
            'symbol': symbol,
            'token': self.finnhub_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('c', 0) == 0:
                return {"error": f"No data found for symbol: {symbol}"}
            
            return {
                'symbol': symbol,
                'current_price': data.get('c', 0),
                'change': data.get('d', 0),
                'percent_change': data.get('dp', 0),
                'high': data.get('h', 0),
                'low': data.get('l', 0),
                'open': data.get('o', 0),
                'previous_close': data.get('pc', 0),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'Finnhub'
            }
        except requests.exceptions.RequestException as e:
            return {"error": f"API Error: {str(e)}"}
    
    def get_stock_price_fcs(self, symbol):
        """
        Fetch current stock price from FCS API
        
        Args:
            symbol (str): Stock symbol (e.g., 'AAPL', 'MSFT')
            
        Returns:
            dict: Stock price data including current, high, low, open, previous close
        """
        if not self.fcs_key:
            return {"error": "FCS API key not configured"}
        
        url = f"{FCS_BASE_URL}/stock/latest"
        params = {
            'symbol': symbol,
            'access_key': self.fcs_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') != True and 'response' not in data:
                return {"error": f"No data found for symbol: {symbol}"}
            
            stock_data = data.get('response', [{}])
            if isinstance(stock_data, list) and len(stock_data) > 0:
                price_info = stock_data[0]
            else:
                price_info = stock_data
            
            current_price = float(price_info.get('c', price_info.get('price', 0)))
            if current_price == 0:
                return {"error": f"No data found for symbol: {symbol}"}
            
            return {
                'symbol': symbol,
                'current_price': current_price,
                'high': float(price_info.get('h', 0)),
                'low': float(price_info.get('l', 0)),
                'open': float(price_info.get('o', 0)),
                'change': float(price_info.get('ch', 0)),
                'percent_change': float(price_info.get('cp', 0)),
                'previous_close': float(price_info.get('pc', 0)),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'FCS API'
            }
        except requests.exceptions.RequestException as e:
            return {"error": f"API Error: {str(e)}"}
        except (ValueError, TypeError) as e:
            return {"error": f"Data parsing error: {str(e)}"}
    
    def get_stock_price(self, symbol):
        """
        Fetch stock price with automatic fallback between APIs
        Tries Finnhub first, then FCS if Finnhub fails
        
        Args:
            symbol (str): Stock symbol (e.g., 'AAPL', 'MSFT')
            
        Returns:
            dict: Stock price data
        """
        # Try Finnhub first
        if self.finnhub_key:
            result = self.get_stock_price_finnhub(symbol)
            if 'error' not in result:
                return result
        
        # Fallback to FCS
        if self.fcs_key:
            result = self.get_stock_price_fcs(symbol)
            if 'error' not in result:
                return result
        
        return {"error": f"Could not fetch price for {symbol} from any API"}
    
    def get_crypto_price(self, symbol):
        """
        Fetch crypto price with automatic fallback between APIs
        Tries Finnhub first, then FCS if Finnhub fails
        
        Args:
            symbol (str): Crypto symbol (e.g., 'BTC', 'ETH')
            
        Returns:
            dict: Crypto price data
        """
        # Try Finnhub first
        if self.finnhub_key:
            result = self.get_crypto_price_finnhub(symbol)
            if 'error' not in result:
                return result
        
        # Fallback to FCS
        if self.fcs_key:
            result = self.get_crypto_price_fcs(symbol)
            if 'error' not in result:
                return result
        
        return {"error": f"Could not fetch price for {symbol} from any API"}
    
    def get_stock_candles_finnhub(self, symbol, resolution='60', count=50):
        """
        Fetch stock candle data from Finnhub API
        
        Args:
            symbol (str): Stock symbol (e.g., 'AAPL', 'MSFT')
            resolution (str): Candle resolution ('1', '5', '15', '60', 'D')
            count (int): Number of candles to fetch
            
        Returns:
            dict: Candle data with OHLCV
        """
        if not self.finnhub_key:
            return {"error": "Finnhub API key not configured"}
        
        import time as time_module
        
        # Calculate time range based on resolution
        now = int(time_module.time())
        
        # Calculate seconds per candle
        if resolution == 'D':
            seconds_per_candle = 86400  # 1 day
        else:
            seconds_per_candle = int(resolution) * 60
        
        # Get enough history for the requested candles
        from_time = now - (seconds_per_candle * count * 2)  # Extra buffer for market hours
        
        url = f"{FINNHUB_BASE_URL}/stock/candle"
        params = {
            'symbol': symbol,
            'resolution': resolution,
            'from': from_time,
            'to': now,
            'token': self.finnhub_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('s') == 'no_data' or not data.get('c'):
                return {"error": f"No candle data found for {symbol}"}
            
            # Get the last candle data
            candles = []
            timestamps = data.get('t', [])
            opens = data.get('o', [])
            highs = data.get('h', [])
            lows = data.get('l', [])
            closes = data.get('c', [])
            volumes = data.get('v', [])
            
            for i in range(min(count, len(closes))):
                idx = -(i + 1)  # Start from most recent
                if abs(idx) <= len(closes):
                    candles.append({
                        'timestamp': datetime.fromtimestamp(timestamps[idx]).strftime('%Y-%m-%d %H:%M'),
                        'open': opens[idx],
                        'high': highs[idx],
                        'low': lows[idx],
                        'close': closes[idx],
                        'volume': volumes[idx] if idx < len(volumes) else 0
                    })
            
            candles.reverse()  # Chronological order
            
            # Current price info from latest candle
            latest_close = closes[-1] if closes else 0
            prev_close = closes[-2] if len(closes) > 1 else latest_close
            change = latest_close - prev_close
            percent_change = (change / prev_close * 100) if prev_close != 0 else 0
            
            return {
                'symbol': symbol,
                'resolution': resolution,
                'timeframe': AVAILABLE_TIMEFRAMES.get(resolution, resolution),
                'current_price': latest_close,
                'change': change,
                'percent_change': percent_change,
                'high': highs[-1] if highs else 0,
                'low': lows[-1] if lows else 0,
                'open': opens[-1] if opens else 0,
                'previous_close': prev_close,
                'candles': candles,
                'candle_count': len(candles),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'Finnhub'
            }
        except requests.exceptions.RequestException as e:
            return {"error": f"API Error: {str(e)}"}
    
    def get_crypto_candles_finnhub(self, symbol, resolution='60', count=50, exchange='binance'):
        """
        Fetch crypto candle data from Finnhub API
        
        Args:
            symbol (str): Crypto symbol (e.g., 'BTC', 'ETH')
            resolution (str): Candle resolution ('1', '5', '15', '60', 'D')
            count (int): Number of candles to fetch
            exchange (str): Exchange to use (default: 'binance')
            
        Returns:
            dict: Candle data with OHLCV
        """
        if not self.finnhub_key:
            return {"error": "Finnhub API key not configured"}
        
        import time as time_module
        
        # Finnhub crypto format
        finnhub_symbol = f"{exchange.upper()}:{symbol.upper()}USDT"
        
        # Calculate time range
        now = int(time_module.time())
        
        if resolution == 'D':
            seconds_per_candle = 86400
        else:
            seconds_per_candle = int(resolution) * 60
        
        from_time = now - (seconds_per_candle * count * 2)
        
        url = f"{FINNHUB_BASE_URL}/crypto/candle"
        params = {
            'symbol': finnhub_symbol,
            'resolution': resolution,
            'from': from_time,
            'to': now,
            'token': self.finnhub_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('s') == 'no_data' or not data.get('c'):
                return {"error": f"No candle data found for {symbol}"}
            
            candles = []
            timestamps = data.get('t', [])
            opens = data.get('o', [])
            highs = data.get('h', [])
            lows = data.get('l', [])
            closes = data.get('c', [])
            volumes = data.get('v', [])
            
            for i in range(min(count, len(closes))):
                idx = -(i + 1)
                if abs(idx) <= len(closes):
                    candles.append({
                        'timestamp': datetime.fromtimestamp(timestamps[idx]).strftime('%Y-%m-%d %H:%M'),
                        'open': opens[idx],
                        'high': highs[idx],
                        'low': lows[idx],
                        'close': closes[idx],
                        'volume': volumes[idx] if idx < len(volumes) else 0
                    })
            
            candles.reverse()
            
            latest_close = closes[-1] if closes else 0
            prev_close = closes[-2] if len(closes) > 1 else latest_close
            change = latest_close - prev_close
            percent_change = (change / prev_close * 100) if prev_close != 0 else 0
            
            return {
                'symbol': symbol,
                'pair': f"{symbol}/USDT",
                'resolution': resolution,
                'timeframe': AVAILABLE_TIMEFRAMES.get(resolution, resolution),
                'current_price': latest_close,
                'change': change,
                'percent_change': percent_change,
                'high': highs[-1] if highs else 0,
                'low': lows[-1] if lows else 0,
                'open': opens[-1] if opens else 0,
                'previous_close': prev_close,
                'candles': candles,
                'candle_count': len(candles),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'Finnhub',
                'exchange': exchange
            }
        except requests.exceptions.RequestException as e:
            return {"error": f"API Error: {str(e)}"}
    
    def get_stock_with_timeframe(self, symbol, resolution='60'):
        """
        Fetch stock data with specified timeframe
        
        Args:
            symbol (str): Stock symbol
            resolution (str): Timeframe resolution
            
        Returns:
            dict: Stock data with candles
        """
        if self.finnhub_key:
            result = self.get_stock_candles_finnhub(symbol, resolution)
            if 'error' not in result:
                return result
        
        # Fallback to basic price if candles not available
        return self.get_stock_price(symbol)
    
    def get_crypto_with_timeframe(self, symbol, resolution='60'):
        """
        Fetch crypto data with specified timeframe
        
        Args:
            symbol (str): Crypto symbol
            resolution (str): Timeframe resolution
            
        Returns:
            dict: Crypto data with candles
        """
        if self.finnhub_key:
            result = self.get_crypto_candles_finnhub(symbol, resolution)
            if 'error' not in result:
                return result
        
        # Fallback to basic price if candles not available
        return self.get_crypto_price(symbol)
    
    def get_crypto_price_finnhub(self, symbol, exchange='binance'):
        """
        Fetch current cryptocurrency price from Finnhub API
        
        Args:
            symbol (str): Crypto symbol (e.g., 'BTC', 'ETH')
            exchange (str): Exchange to use (default: 'binance')
            
        Returns:
            dict: Crypto price data
        """
        if not self.finnhub_key:
            return {"error": "Finnhub API key not configured"}
        
        # Finnhub uses format like 'BINANCE:BTCUSDT'
        finnhub_symbol = f"{exchange.upper()}:{symbol.upper()}USDT"
        
        url = f"{FINNHUB_BASE_URL}/quote"
        params = {
            'symbol': finnhub_symbol,
            'token': self.finnhub_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('c', 0) == 0:
                return {"error": f"No data found for crypto: {symbol}"}
            
            return {
                'symbol': symbol,
                'pair': f"{symbol}/USDT",
                'current_price': data.get('c', 0),
                'change': data.get('d', 0),
                'percent_change': data.get('dp', 0),
                'high': data.get('h', 0),
                'low': data.get('l', 0),
                'open': data.get('o', 0),
                'previous_close': data.get('pc', 0),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'Finnhub',
                'exchange': exchange
            }
        except requests.exceptions.RequestException as e:
            return {"error": f"API Error: {str(e)}"}
    
    def get_crypto_price_fcs(self, symbol):
        """
        Fetch current cryptocurrency price from FCS API
        
        Args:
            symbol (str): Crypto symbol (e.g., 'BTC', 'ETH')
            
        Returns:
            dict: Crypto price data
        """
        if not self.fcs_key:
            return {"error": "FCS API key not configured"}
        
        url = f"{FCS_BASE_URL}/crypto/latest"
        params = {
            'symbol': f"{symbol}/USD",
            'access_key': self.fcs_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') != True and 'response' not in data:
                return {"error": f"No data found for crypto: {symbol}"}
            
            crypto_data = data.get('response', [{}])
            if isinstance(crypto_data, list) and len(crypto_data) > 0:
                price_info = crypto_data[0]
            else:
                price_info = crypto_data
            
            return {
                'symbol': symbol,
                'pair': f"{symbol}/USD",
                'current_price': float(price_info.get('c', price_info.get('price', 0))),
                'high': float(price_info.get('h', 0)),
                'low': float(price_info.get('l', 0)),
                'open': float(price_info.get('o', 0)),
                'change': float(price_info.get('ch', 0)),
                'percent_change': float(price_info.get('cp', 0)),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'FCS API'
            }
        except requests.exceptions.RequestException as e:
            return {"error": f"API Error: {str(e)}"}
        except (ValueError, TypeError) as e:
            return {"error": f"Data parsing error: {str(e)}"}
    
    def get_all_sample_prices(self):
        """
        Fetch prices for all sample assets (Bitcoin, Ethereum, Nifty 50, Apple)
        
        Returns:
            dict: Dictionary containing all price data
        """
        results = {
            'stocks': [],
            'cryptos': [],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Sample Stocks
        stocks = [
            {'symbol': 'AAPL', 'name': 'Apple Inc.'},
            {'symbol': '^NSEI', 'name': 'Nifty 50'}  # Note: May need different symbol based on API
        ]
        
        # Sample Cryptocurrencies
        cryptos = [
            {'symbol': 'BTC', 'name': 'Bitcoin'},
            {'symbol': 'ETH', 'name': 'Ethereum'}
        ]
        
        # Fetch stock prices (with automatic fallback)
        for stock in stocks:
            price_data = self.get_stock_price(stock['symbol'])
            price_data['name'] = stock['name']
            results['stocks'].append(price_data)
        
        # Fetch crypto prices (with automatic fallback)
        for crypto in cryptos:
            price_data = self.get_crypto_price(crypto['symbol'])
            price_data['name'] = crypto['name']
            results['cryptos'].append(price_data)
        
        return results


def display_price_card(data, asset_type, show_candles=False):
    """Display a price card in Streamlit"""
    if 'error' in data:
        st.error(f"❌ {data.get('name', 'Unknown')}: {data['error']}")
        return
    
    name = data.get('name', data.get('symbol', data.get('pair', 'Unknown')))
    current_price = data.get('current_price', 0) or 0
    change = data.get('change', 0) or 0
    percent_change = data.get('percent_change', 0) or 0
    timeframe = data.get('timeframe', '')
    
    # Determine color based on change
    color = "green" if change >= 0 else "red"
    arrow = "↑" if change >= 0 else "↓"
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**{name}**")
        if asset_type == 'crypto':
            st.caption(f"Pair: {data.get('pair', 'N/A')}")
        else:
            st.caption(f"Symbol: {data.get('symbol', 'N/A')}")
        if timeframe:
            st.caption(f"⏱️ Timeframe: {timeframe}")
    
    with col2:
        st.metric(label="Price", value=f"${current_price:,.2f}")
    
    with col3:
        st.metric(
            label="Change",
            value=f"{arrow} {abs(percent_change):.2f}%",
            delta=f"{change:+.2f}" if change != 0 else None
        )
    
    # Additional details
    with st.expander("View Details"):
        detail_cols = st.columns(4)
        with detail_cols[0]:
            st.metric("Open", f"{(data.get('open', 0) or 0):,.4f}")
        with detail_cols[1]:
            st.metric("High", f"{(data.get('high', 0) or 0):,.4f}")
        with detail_cols[2]:
            st.metric("Low", f"{(data.get('low', 0) or 0):,.4f}")
        with detail_cols[3]:
            st.metric("Prev Close", f"{(data.get('previous_close', 0) or 0):,.4f}")
        st.caption(f"Source: {data.get('source', 'N/A')} | Last Updated: {data.get('timestamp', 'N/A')}")
    
    # Show candle data if available
    if show_candles and 'candles' in data and data['candles']:
        with st.expander(f"📊 Candle Data ({data.get('candle_count', 0)} candles)"):
            candle_df = pd.DataFrame(data['candles'])
            st.dataframe(candle_df, use_container_width=True, hide_index=True)
            
            # Simple price chart
            if len(candle_df) > 1:
                st.line_chart(candle_df.set_index('timestamp')['close'])


def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="Trading Coach - Live Prices",
        page_icon="📈",
        layout="wide"
    )
    
    st.title("📈 Trading Coach - Live Price Dashboard")
    st.markdown("Real-time prices for stocks and cryptocurrencies using Finnhub and FCS APIs")
    
    # Sidebar for API key configuration
    st.sidebar.header("⚙️ API Configuration")
    
    finnhub_key = st.sidebar.text_input(
        "Finnhub API Key",
        value=FINNHUB_API_KEY,
        type="password",
        help="Get your free API key from https://finnhub.io/register"
    )
    
    fcs_key = st.sidebar.text_input(
        "FCS API Key",
        value=FCS_API_KEY,
        type="password",
        help="Get your free API key from https://fcsapi.com/"
    )
    
    if not finnhub_key and not fcs_key:
        st.warning("⚠️ Please configure at least one API key in the sidebar to fetch live prices.")
        st.info("""
        **How to get API keys:**
        - **Finnhub**: Sign up at [finnhub.io](https://finnhub.io/register) for free API access
        - **FCS API**: Sign up at [fcsapi.com](https://fcsapi.com/) for forex and crypto data
        """)
        return
    
    # Initialize Trading Coach
    coach = TradingCoach(finnhub_key=finnhub_key, fcs_key=fcs_key)
    
    # Tabs for different asset types
    tab1, tab2, tab3 = st.tabs(["📊 All Assets", "💹 Stocks", "₿ Crypto"])
    
    # Custom asset input section
    st.sidebar.header("🔍 Custom Asset Lookup")
    
    asset_type = st.sidebar.selectbox(
        "Asset Type",
        ["Stock", "Cryptocurrency"]
    )
    
    if asset_type == "Stock":
        custom_symbol = st.sidebar.text_input("Stock Symbol", placeholder="e.g., AAPL, MSFT, GOOGL")
        if st.sidebar.button("Fetch Stock Price"):
            if custom_symbol:
                with st.spinner(f"Fetching {custom_symbol} (trying Finnhub → FCS)..."):
                    result = coach.get_stock_price(custom_symbol.upper())
                st.sidebar.json(result)
    
    else:  # Cryptocurrency
        custom_crypto = st.sidebar.text_input("Crypto Symbol", placeholder="e.g., BTC, ETH, SOL")
        if st.sidebar.button("Fetch Crypto Price"):
            if custom_crypto:
                with st.spinner(f"Fetching {custom_crypto} (trying Finnhub → FCS)..."):
                    result = coach.get_crypto_price(custom_crypto.upper())
                st.sidebar.json(result)
    
    # Refresh button
    if st.button("🔄 Refresh All Prices", type="primary"):
        st.cache_data.clear()
    
    # Tab 1: All Assets Overview
    with tab1:
        st.subheader("📊 Quick Asset Overview")
        
        # Show available asset counts
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Available Stocks", len(AVAILABLE_STOCKS))
        with col2:
            st.metric("Available Cryptos", len(AVAILABLE_CRYPTOS))
        
        st.markdown("---")
        st.markdown("### 🚀 Quick Price Check")
        st.markdown("Select assets from each category to view their prices instantly:")
        
        # Quick select section
        quick_col1, quick_col2 = st.columns(2)
        
        with quick_col1:
            st.markdown("**💹 Quick Stock**")
            quick_stock = st.selectbox(
                "Select a stock:",
                options=[""] + [f"{s} - {n}" for s, n in AVAILABLE_STOCKS.items()],
                key="quick_stock"
            )
        
        with quick_col2:
            st.markdown("**₿ Quick Crypto**")
            quick_crypto = st.selectbox(
                "Select a crypto:",
                options=[""] + [f"{s} - {n}" for s, n in AVAILABLE_CRYPTOS.items()],
                key="quick_crypto"
            )
        
        if st.button("⚡ Fetch Quick Prices", type="primary", key="quick_fetch"):
            st.markdown("---")
            result_cols = st.columns(2)
            
            with result_cols[0]:
                if quick_stock:
                    symbol = quick_stock.split(" - ")[0]
                    name = quick_stock.split(" - ")[1]
                    with st.spinner(f"Fetching {symbol}..."):
                        data = coach.get_stock_price(symbol)
                        data['name'] = name
                        display_price_card(data, 'stock')
            
            with result_cols[1]:
                if quick_crypto:
                    symbol = quick_crypto.split(" - ")[0]
                    name = quick_crypto.split(" - ")[1]
                    with st.spinner(f"Fetching {symbol}..."):
                        data = coach.get_crypto_price(symbol)
                        data['name'] = name
                        display_price_card(data, 'crypto')
        
        # Show all available assets in expandable sections
        st.markdown("---")
        st.markdown("### 📋 Available Assets List")
        
        with st.expander("📈 View All Available Stocks"):
            stock_df = pd.DataFrame([
                {"Symbol": symbol, "Company": name, "Category": "Stock"}
                for symbol, name in AVAILABLE_STOCKS.items()
            ])
            st.dataframe(stock_df, use_container_width=True, hide_index=True)
        
        with st.expander("₿ View All Available Cryptocurrencies"):
            crypto_df = pd.DataFrame([
                {"Symbol": symbol, "Name": name, "Category": "Cryptocurrency"}
                for symbol, name in AVAILABLE_CRYPTOS.items()
            ])
            st.dataframe(crypto_df, use_container_width=True, hide_index=True)
    
    # Tab 2: Stocks
    with tab2:
        st.subheader("💹 Stock Prices")
        
        # Stock selector from available list
        st.markdown("### 📋 Select Stocks to View")
        
        # Timeframe selection for stocks
        stock_tf_col1, stock_tf_col2 = st.columns([3, 1])
        with stock_tf_col2:
            stock_timeframe = st.selectbox(
                "⏱️ Timeframe",
                options=list(AVAILABLE_TIMEFRAMES.keys()),
                format_func=lambda x: AVAILABLE_TIMEFRAMES[x],
                index=3,  # Default to 1 Hour
                key="stock_timeframe"
            )
            show_stock_candles = st.checkbox("Show Candles", value=True, key="show_stock_candles")
        
        # Create display options for multiselect
        stock_options = [f"{symbol} - {name}" for symbol, name in AVAILABLE_STOCKS.items()]
        
        with stock_tf_col1:
            selected_stocks = st.multiselect(
                "Choose stocks from the list below:",
                options=stock_options,
                default=["AAPL - Apple Inc.", "MSFT - Microsoft Corporation", "GOOGL - Alphabet Inc. (Google)", "TSLA - Tesla Inc."],
                help="Select multiple stocks to view their current prices"
            )
        
        if selected_stocks:
            if st.button("📊 Fetch Selected Stock Prices", key="fetch_stocks"):
                st.markdown("---")
                st.info(f"📊 Fetching data with **{AVAILABLE_TIMEFRAMES[stock_timeframe]}** timeframe")
                
                # Create columns for displaying stocks
                cols = st.columns(2)
                
                for idx, stock_display in enumerate(selected_stocks):
                    symbol = stock_display.split(" - ")[0]
                    name = stock_display.split(" - ")[1]
                    
                    with cols[idx % 2]:
                        with st.spinner(f"Fetching {symbol}..."):
                            price_data = coach.get_stock_with_timeframe(symbol, stock_timeframe)
                            price_data['name'] = name
                            display_price_card(price_data, 'stock', show_candles=show_stock_candles)
                            st.divider()
        else:
            st.info("Please select at least one stock from the dropdown above.")
    
    # Tab 3: Cryptocurrencies
    with tab3:
        st.subheader("₿ Cryptocurrency Prices")
        
        # Crypto selector from available list
        st.markdown("### 📋 Select Cryptocurrencies to View")
        
        # Timeframe selection for crypto
        crypto_tf_col1, crypto_tf_col2 = st.columns([3, 1])
        with crypto_tf_col2:
            crypto_timeframe = st.selectbox(
                "⏱️ Timeframe",
                options=list(AVAILABLE_TIMEFRAMES.keys()),
                format_func=lambda x: AVAILABLE_TIMEFRAMES[x],
                index=3,  # Default to 1 Hour
                key="crypto_timeframe"
            )
            show_crypto_candles = st.checkbox("Show Candles", value=True, key="show_crypto_candles")
        
        # Create display options for multiselect
        crypto_options = [f"{symbol} - {name}" for symbol, name in AVAILABLE_CRYPTOS.items()]
        
        with crypto_tf_col1:
            selected_cryptos = st.multiselect(
                "Choose cryptocurrencies from the list below:",
                options=crypto_options,
                default=["BTC - Bitcoin", "ETH - Ethereum", "SOL - Solana", "DOGE - Dogecoin"],
                help="Select multiple cryptocurrencies to view their current prices"
            )
        
        if selected_cryptos:
            if st.button("₿ Fetch Selected Crypto Prices", key="fetch_cryptos"):
                st.markdown("---")
                st.info(f"📊 Fetching data with **{AVAILABLE_TIMEFRAMES[crypto_timeframe]}** timeframe")
                
                # Create columns for displaying cryptos
                cols = st.columns(2)
                
                for idx, crypto_display in enumerate(selected_cryptos):
                    symbol = crypto_display.split(" - ")[0]
                    name = crypto_display.split(" - ")[1]
                    
                    with cols[idx % 2]:
                        with st.spinner(f"Fetching {symbol}..."):
                            price_data = coach.get_crypto_with_timeframe(symbol, crypto_timeframe)
                            price_data['name'] = name
                            display_price_card(price_data, 'crypto', show_candles=show_crypto_candles)
                            st.divider()
        else:
            st.info("Please select at least one cryptocurrency from the dropdown above.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p><strong>Trading Coach</strong> - Powered by Finnhub and FCS APIs</p>
        <p>📈 Stocks | ₿ Crypto</p>
        <p><small>Data is for informational purposes only. Not financial advice.</small></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
