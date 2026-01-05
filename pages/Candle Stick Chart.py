import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import talib
import numpy as np
import sys
import os
import requests

# Add parent path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.styles import get_tradeguide_styles, get_sidebar_html, get_page_header

# Page config
st.set_page_config(layout="wide", page_title="Candlestick Charts - TradeGuide AI", page_icon="🕯️")

# Apply shared styles
st.markdown(get_tradeguide_styles(), unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # Branding - icon and title
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; padding: 10px 0 15px 0; border-bottom: 1px solid #e2e8f0; margin-bottom: 15px;">
        <span style="font-size: 28px;">📈</span>
        <span style="font-size: 1.1rem; font-weight: 700; color: #1e293b;">Trade<span style='color: #0ea5e9;'>Guide</span> AI</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="nav-section-label">Navigation</div>', unsafe_allow_html=True)
    st.page_link("Home Page.py", label="🏠  Home")
    st.page_link("pages/Trading_Dashboard.py", label="📊  Trading Dashboard")
    st.page_link("pages/Technical_Analysis.py", label="📈  Technical Analysis")
    st.page_link("pages/Strategy_Developer.py", label="🎯  Strategy Developer")
    st.page_link("pages/Investment_Strategist.py", label="💡  Investment Strategist")
    st.page_link("pages/Candle Stick Chart.py", label="🕯️  Candlestick Charts")

# Page Header
st.markdown(get_page_header("🕯️ Candlestick Charts", "Learn to read candlestick patterns with interactive charts"), unsafe_allow_html=True)

# Define colors for multi-stock comparison
COLORS = ["blue", "red", "green", "orange", "purple", "cyan", "magenta", "yellow"]

# Fetch S&P 500 companies
@st.cache_data
def get_sp500_components():
    try:
        # Method 1: Try with requests library and custom headers
        try:
            import requests
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
            }
            url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            df = pd.read_html(response.text)[0]
            tickers = df["Symbol"].to_list()
            tickers_companies_dict = dict(zip(df["Symbol"], df["Security"]))
            return tickers, tickers_companies_dict
        except ImportError:
            # Method 2: Fallback to urllib with headers
            import urllib.request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            req = urllib.request.Request(
                "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
                headers=headers
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read()
                df = pd.read_html(html)[0]
                tickers = df["Symbol"].to_list()
                tickers_companies_dict = dict(zip(df["Symbol"], df["Security"]))
                return tickers, tickers_companies_dict
    except Exception as e:
        st.error(f"Error fetching S&P 500 components: {e}")
        # Fallback: Return a default list of popular stocks
        default_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "JPM", "V", "JNJ", 
                          "WMT", "PG", "MA", "HD", "DIS", "NFLX", "BAC", "ADBE", "CRM", "CSCO"]
        default_dict = {ticker: ticker for ticker in default_tickers}
        st.warning("Using default stock list. Please check your internet connection.")
        return default_tickers, default_dict

# Load data from Yahoo Finance
@st.cache_data
def load_data_yfinance(symbol, start_date, end_date, interval="1d"):
    try:
        df = yf.download(symbol, start=start_date, end=end_date, interval=interval, progress=False)
        if df.empty:
            st.error(f"No data found for {symbol}")
            return None
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
        df = df.dropna()
        df.index.name = 'Date'
        df.index = pd.to_datetime(df.index, utc=True)  # Ensure UTC timezone
        return df
    except Exception as e:
        st.error(f"Error fetching data from Yahoo Finance: {e}")
        return None

# Fetch financial metrics
@st.cache_data
def get_financial_metrics(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return {
            "P/E Ratio": info.get("trailingPE", "N/A"),
            "Market Cap": info.get("marketCap", "N/A"),
            "Dividend Yield": info.get("dividendYield", "N/A")
        }
    except Exception as e:
        st.error(f"Error fetching financial metrics for {symbol}: {e}")
        return {"P/E Ratio": "N/A", "Market Cap": "N/A", "Dividend Yield": "N/A"}

# Fetch market status from Finnhub
@st.cache_data(ttl=60)
def get_market_status(api_key):
    try:
        url = f"https://finnhub.io/api/v1/stock/market-status?exchange=US&token={api_key}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                "exchange": data.get("exchange", "US"),
                "timezone": data.get("timezone", "America/New_York"),
                "status": data.get("isOpen", False),
                "session": data.get("session", "N/A")
            }
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching market status: {e}")
        return None

# Fetch general market news from Finnhub
@st.cache_data(ttl=300)
def get_market_news(api_key, category="general"):
    try:
        url = f"https://finnhub.io/api/v1/news?category={category}&token={api_key}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            news = response.json()[:5]  # Get top 5 news
            return [{"title": item.get("headline", "No title"), 
                    "link": item.get("url", "#"),
                    "source": item.get("source", "Unknown"),
                    "summary": item.get("summary", "")[:150] + "..." if item.get("summary") else ""} 
                   for item in news]
        else:
            return []
    except Exception as e:
        st.error(f"Error fetching market news: {e}")
        return []

# Fetch company-specific news from Finnhub
@st.cache_data(ttl=300)
def get_company_news(symbol, api_key, from_date=None, to_date=None):
    try:
        if not from_date:
            from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        if not to_date:
            to_date = datetime.now().strftime("%Y-%m-%d")
        
        url = f"https://finnhub.io/api/v1/company-news?symbol={symbol}&from={from_date}&to={to_date}&token={api_key}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            news = response.json()[:5]  # Get top 5 news
            return [{"title": item.get("headline", "No title"), 
                    "link": item.get("url", "#"),
                    "source": item.get("source", "Unknown"),
                    "datetime": datetime.fromtimestamp(item.get("datetime", 0)).strftime("%Y-%m-%d %H:%M") if item.get("datetime") else "N/A",
                    "summary": item.get("summary", "")[:150] + "..." if item.get("summary") else ""} 
                   for item in news]
        else:
            return []
    except Exception as e:
        st.error(f"Error fetching company news for {symbol}: {e}")
        return []

# Process data with technical indicators and candlestick patterns
@st.cache_data
def process_data(df, symbol):
    try:
        df = df.copy()
        df["BarColor"] = np.where(df["Open"] > df["Close"], "red", "green")
        df["Date_str"] = df.index.strftime("%Y-%m-%d %H:%M:%S")
        
        if not isinstance(df["Close"], pd.Series):
            st.error("Close column is not a valid Series. Check data structure.")
            return None, None
        
        close_array = df["Close"].to_numpy()
        if close_array.ndim != 1:
            st.error(f"Close array has incorrect dimensions: {close_array.ndim}D instead of 1D")
            return None, None

        df["SMA"] = talib.SMA(close_array, timeperiod=3)
        df["MA"] = talib.MA(close_array, timeperiod=3)
        df["EMA"] = talib.EMA(close_array, timeperiod=3)
        df["WMA"] = talib.WMA(close_array, timeperiod=3)
        df["RSI"] = talib.RSI(close_array, timeperiod=3)
        df["MOM"] = talib.MOM(close_array, timeperiod=3)
        df["DEMA"] = talib.DEMA(close_array, timeperiod=3)
        df["TEMA"] = talib.TEMA(close_array, timeperiod=3)

        patterns = {
            "Doji": talib.CDLDOJI(df["Open"].to_numpy(), df["High"].to_numpy(), df["Low"].to_numpy(), df["Close"].to_numpy()),
            "Hammer": talib.CDLHAMMER(df["Open"].to_numpy(), df["High"].to_numpy(), df["Low"].to_numpy(), df["Close"].to_numpy()),
            "Bullish Engulfing": talib.CDLENGULFING(df["Open"].to_numpy(), df["High"].to_numpy(), df["Low"].to_numpy(), df["Close"].to_numpy())
        }
        pattern_df = pd.DataFrame(patterns, index=df.index)
        pattern_df = pattern_df[pattern_df != 0].dropna(how='all').reset_index()
        pattern_df["Symbol"] = symbol
        pattern_df["Date"] = pattern_df["Date"].dt.strftime("%Y-%m-%d %H:%M:%S")

        return df.reset_index(), pattern_df
    except Exception as e:
        st.error(f"Error processing data: {e}")
        return None, None

# Calculate performance metrics
@st.cache_data
def calculate_performance_metrics(df):
    try:
        returns = df["Close"].pct_change().dropna()
        cumulative_return = (1 + returns).cumprod().iloc[-1] - 1
        annualized_volatility = returns.std() * np.sqrt(252)
        max_drawdown = (df["Close"].cummax() - df["Close"]).max() / df["Close"].cummax().max()
        return {
            "Cumulative Return": cumulative_return * 100,
            "Annualized Volatility": annualized_volatility * 100,
            "Max Drawdown": max_drawdown * 100
        }
    except Exception as e:
        st.error(f"Error calculating performance metrics: {e}")
        return {"Cumulative Return": "N/A", "Annualized Volatility": "N/A", "Max Drawdown": "N/A"}

# Backtest SMA crossover strategy
@st.cache_data
def backtest_sma_crossover(df):
    try:
        df = df.copy()
        df["SMA_Short"] = talib.SMA(df["Close"].to_numpy(), timeperiod=10)
        df["SMA_Long"] = talib.SMA(df["Close"].to_numpy(), timeperiod=50)
        df["Signal"] = np.where(df["SMA_Short"] > df["SMA_Long"], 1, 0)
        df["Position"] = df["Signal"].diff()
        df["Returns"] = df["Close"].pct_change()
        df["Strategy_Returns"] = df["Returns"] * df["Signal"].shift(1)
        cumulative_strategy_return = (1 + df["Strategy_Returns"].dropna()).cumprod().iloc[-1] - 1
        return cumulative_strategy_return * 100
    except Exception as e:
        st.error(f"Error backtesting strategy: {e}")
        return "N/A"

# Convert dataframe to downloadable CSV
@st.cache_data
def convert_df_to_csv(df):
    df = df.copy()
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d %H:%M:%S")
    return df.to_csv(index=False).encode("utf-8")

# Create candlestick chart with multiple stocks using Plotly
indicator_colors = {"SMA": "orange", "EMA": "violet", "WMA": "blue", "RSI": "yellow", "MOM": "black", "DEMA": "red", 
                    "MA": "tomato", "TEMA": "dodgerblue"}

def create_chart(dfs, symbols, close_line=False, include_vol=False, indicators=[], price_alerts=None, multi_stock=False):
    # Create subplots with volume if needed
    if include_vol and not multi_stock:
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                           vertical_spacing=0.03, 
                           row_heights=[0.7, 0.3],
                           subplot_titles=('Price', 'Volume'))
    else:
        fig = go.Figure()
    
    for idx, (df, symbol) in enumerate(zip(dfs, symbols)):
        if multi_stock:
            df["Normalized_Close"] = df["Close"] / df["Close"].iloc[0]
            color = COLORS[idx % len(COLORS)]
            trace = go.Scatter(x=df["Date"], y=df["Normalized_Close"], 
                             mode='lines', name=symbol, line=dict(color=color))
            fig.add_trace(trace)
        else:
            # Add candlestick
            candlestick = go.Candlestick(
                x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name=symbol,
                increasing_line_color='green',
                decreasing_line_color='red'
            )
            
            if include_vol:
                fig.add_trace(candlestick, row=1, col=1)
            else:
                fig.add_trace(candlestick)
            
            # Add close line if requested
            if close_line:
                close_trace = go.Scatter(x=df['Date'], y=df['Close'], 
                                       mode='lines', name='Close', 
                                       line=dict(color='black', width=1))
                if include_vol:
                    fig.add_trace(close_trace, row=1, col=1)
                else:
                    fig.add_trace(close_trace)
            
            # Add technical indicators
            for indicator in indicators:
                if indicator in df.columns:
                    ind_trace = go.Scatter(x=df['Date'], y=df[indicator], 
                                         mode='lines', name=indicator,
                                         line=dict(color=indicator_colors.get(indicator, 'gray'), width=2))
                    if include_vol:
                        fig.add_trace(ind_trace, row=1, col=1)
                    else:
                        fig.add_trace(ind_trace)
            
            # Add volume bars
            if include_vol:
                colors = ['red' if df['Open'].iloc[i] > df['Close'].iloc[i] else 'green' 
                         for i in range(len(df))]
                volume_trace = go.Bar(x=df['Date'], y=df['Volume'], 
                                    name='Volume', marker_color=colors, 
                                    showlegend=False)
                fig.add_trace(volume_trace, row=2, col=1)
    
    # Add price alerts
    if price_alerts and not multi_stock:
        for level, color in price_alerts.items():
            alert_line = go.Scatter(
                x=[dfs[0]['Date'].min(), dfs[0]['Date'].max()],
                y=[level, level],
                mode='lines',
                name=f'Alert ${level}',
                line=dict(color=color, dash='dash', width=2)
            )
            if include_vol:
                fig.add_trace(alert_line, row=1, col=1)
            else:
                fig.add_trace(alert_line)
    
    # Update layout
    fig.update_layout(
        height=650 if include_vol else 500,
        xaxis_title='Date',
        yaxis_title='Price ($)' if not multi_stock else 'Normalized Price',
        hovermode='x unified',
        template='plotly_white',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    if include_vol and not multi_stock:
        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_yaxes(title_text="Price ($)", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)
    
    fig.update_xaxes(rangeslider_visible=False)
    
    return fig

# Dashboard
st.title(":green[Candle]:red[stick] Pattern Technical Analysis :tea: :coffee:")

# Sidebar for controls
st.sidebar.markdown("#### 🔑 Finnhub API Key")
finnhub_api_key = st.sidebar.text_input(
    "Enter Finnhub API Key",
    type="password",
    value=os.getenv("FINNHUB_API_KEY", ""),
    help="Get your free API key from https://finnhub.io/"
)
if finnhub_api_key:
    os.environ["FINNHUB_API_KEY"] = finnhub_api_key
    st.sidebar.success("✅ API key set")
else:
    st.sidebar.warning("⚠️ Finnhub API key required for news")

st.sidebar.markdown("---")
st.sidebar.markdown("#### S&P 500 Company Selection")
tickers, tickers_companies_dict = get_sp500_components()
if tickers:
    selected_companies = st.sidebar.multiselect("Select Companies", 
                                              options=tickers, 
                                              default=["AAPL"],
                                              format_func=lambda x: f"{x} - {tickers_companies_dict.get(x, x)}")
else:
    st.error("No S&P 500 companies available.")
    selected_companies = []

st.sidebar.markdown("#### Data Interval")
interval = st.sidebar.selectbox("Select Interval", ["1d", "1h", "30m"], index=0)

st.sidebar.markdown("#### Date Range Selection")
# Adjust max date range based on interval
max_date = datetime(2024, 12, 31)
if interval in ["1h", "30m"]:
    max_date = datetime.now().date()
    default_end = max_date
    default_start = max_date - timedelta(days=7)
else:
    default_end = datetime(2022, 12, 31)
    default_start = datetime(2022, 1, 1)

col1, col2 = st.sidebar.columns(2, gap="medium")
with col1:
    start_dt = st.date_input("Start:", value=default_start, min_value=datetime(2020, 1, 1), max_value=max_date)
with col2:
    end_dt = st.date_input("End:", value=default_end, min_value=datetime(2020, 1, 1), max_value=max_date)

multi_stock = st.sidebar.checkbox("Compare Multiple Stocks", value=False)
close_line = st.sidebar.checkbox("Close Prices", disabled=multi_stock)
volume = st.sidebar.checkbox("Include Volume", disabled=multi_stock)

talib_indicators = ["MA", "EMA", "SMA", "WMA", "RSI", "MOM", "DEMA", "TEMA"]
indicators = st.sidebar.multiselect(label="Technical Indicators", options=talib_indicators, disabled=multi_stock)

# Price alerts
st.sidebar.markdown("#### Price Alerts")
upper_alert = st.sidebar.number_input("Upper Price Alert", min_value=0.0, step=1.0, value=0.0)
lower_alert = st.sidebar.number_input("Lower Price Alert", min_value=0.0, step=1.0, value=0.0)
price_alerts = {}
if upper_alert > 0:
    price_alerts[upper_alert] = "red"
if lower_alert > 0:
    price_alerts[lower_alert] = "blue"

# Load and process data
if selected_companies:
    dfs = []
    pattern_dfs = []
    for company in selected_companies:
        raw_df = load_data_yfinance(company, start_dt, end_dt, interval=interval)
        if raw_df is not None:
            processed_df, pattern_df = process_data(raw_df, company)
            if processed_df is not None:
                # Convert start_dt and end_dt to datetime64[ns, UTC]
                start_dt_utc = pd.to_datetime(start_dt).tz_localize('UTC')
                end_dt_utc = pd.to_datetime(end_dt).tz_localize('UTC')
                sub_df = processed_df[(processed_df['Date'] >= start_dt_utc) & 
                                     (processed_df['Date'] <= end_dt_utc)]
                if not sub_df.empty:
                    dfs.append(sub_df)
                    if not pattern_df.empty:
                        pattern_dfs.append(pattern_df)
                else:
                    st.error(f"No data available for {company} in the selected date range.")
            else:
                st.error(f"Failed to process data for {company}.")
        else:
            st.error(f"Failed to load data for {company}.")

    if dfs:
        st.plotly_chart(create_chart(dfs, selected_companies, close_line, volume, indicators, price_alerts, multi_stock), use_container_width=True)

        for company, df in zip(selected_companies, dfs):
            with st.expander(f"Metrics for {company}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("##### Financial Metrics")
                    metrics = get_financial_metrics(company)
                    st.metric("P/E Ratio", f"{metrics['P/E Ratio']:.2f}" if isinstance(metrics['P/E Ratio'], (int, float)) else metrics['P/E Ratio'])
                    st.metric("Market Cap", f"${metrics['Market Cap']/1e9:.2f}B" if isinstance(metrics['Market Cap'], (int, float)) else metrics['Market Cap'])
                    st.metric("Dividend Yield", f"{metrics['Dividend Yield']*100:.2f}%" if isinstance(metrics['Dividend Yield'], (int, float)) else metrics['Dividend Yield'])
                with col2:
                    st.markdown("##### Performance Metrics")
                    perf_metrics = calculate_performance_metrics(df)
                    st.metric("Cumulative Return", f"{perf_metrics['Cumulative Return']:.2f}%" if isinstance(perf_metrics['Cumulative Return'], (int, float)) else perf_metrics['Cumulative Return'])
                    st.metric("Annualized Volatility", f"{perf_metrics['Annualized Volatility']:.2f}%" if isinstance(perf_metrics['Annualized Volatility'], (int, float)) else perf_metrics['Annualized Volatility'])
                    st.metric("Max Drawdown", f"{perf_metrics['Max Drawdown']:.2f}%" if isinstance(perf_metrics['Max Drawdown'], (int, float)) else perf_metrics['Max Drawdown'])

                st.markdown("##### SMA Crossover Strategy")
                strategy_return = backtest_sma_crossover(df)
                st.metric("Strategy Cumulative Return", f"{strategy_return:.2f}%" if isinstance(strategy_return, (int, float)) else strategy_return)

                csv = convert_df_to_csv(df)
                st.download_button(
                    label=f"Download {company} Data as CSV",
                    data=csv,
                    file_name=f"{company}_data.csv",
                    mime="text/csv",
                )

        if pattern_dfs:
            st.markdown("#### Detected Candlestick Patterns")
            combined_patterns = pd.concat(pattern_dfs)
            st.dataframe(combined_patterns[["Symbol", "Date", "Doji", "Hammer", "Bullish Engulfing"]])

        # Market Status and News Section
        if finnhub_api_key:
            st.markdown("---")
            st.markdown("### 📰 News & Market Information")
            
            # Market Status
            with st.expander("📊 Market Status", expanded=True):
                market_status = get_market_status(finnhub_api_key)
                if market_status:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Exchange", market_status["exchange"])
                    with col2:
                        st.metric("Status", "🟢 Open" if market_status["status"] else "🔴 Closed")
                    with col3:
                        st.metric("Timezone", market_status["timezone"])
                    with col4:
                        st.metric("Session", market_status["session"])
                else:
                    st.info("Market status unavailable")
            
            # General Market News
            with st.expander("🌍 Market News", expanded=False):
                market_news = get_market_news(finnhub_api_key, category="general")
                if market_news:
                    for item in market_news:
                        st.markdown(f"**[{item['title']}]({item['link']})**")
                        st.caption(f"Source: {item['source']}")
                        if item['summary']:
                            st.markdown(f"{item['summary']}")
                        st.markdown("---")
                else:
                    st.info("No market news available")
            
            # Company-specific News
            for company in selected_companies:
                with st.expander(f"🏢 Company News: {company}", expanded=False):
                    company_news = get_company_news(company, finnhub_api_key)
                    if company_news:
                        for item in company_news:
                            st.markdown(f"**[{item['title']}]({item['link']})**")
                            col1, col2 = st.columns(2)
                            with col1:
                                st.caption(f"📅 {item['datetime']}")
                            with col2:
                                st.caption(f"📰 {item['source']}")
                            if item['summary']:
                                st.markdown(f"{item['summary']}")
                            st.markdown("---")
                    else:
                        st.info(f"No news available for {company}")
        else:
            st.info("💡 Enter your Finnhub API key in the sidebar to view market status and news")
else:
    st.info("Please select at least one company to display the chart.")