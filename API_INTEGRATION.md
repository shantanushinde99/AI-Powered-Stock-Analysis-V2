# Alpha Vantage and Yahoo Finance API Integration

## Overview

This project now uses **Alpha Vantage API** as the primary data source with **Yahoo Finance** as an automatic fallback for all trading agents. This dual-source architecture ensures maximum reliability and data coverage for stock analysis.

## Architecture

### Data Vendor System

The project uses a sophisticated routing system that automatically manages API calls across multiple data vendors:

1. **Primary Source**: Alpha Vantage API (professional-grade financial data)
2. **Fallback Source**: Yahoo Finance (real-time market data)
3. **Automatic Failover**: If Alpha Vantage hits rate limits or fails, the system automatically falls back to Yahoo Finance

### Supported Data Categories

#### 1. Core Stock APIs (`core_stock_apis`)
- **Primary**: Alpha Vantage Time Series
- **Fallback**: Yahoo Finance Historical Data
- **Functions**: `get_stock_data(symbol, start_date, end_date)`
- **Returns**: OHLCV (Open, High, Low, Close, Volume) price data

#### 2. Technical Indicators (`technical_indicators`)
- **Primary**: Alpha Vantage Technical Indicators
- **Fallback**: Yahoo Finance + Stockstats calculation
- **Functions**: `get_indicators(symbol, indicator, curr_date, look_back_days)`
- **Supported Indicators**:
  - Moving Averages: `close_50_sma`, `close_200_sma`, `close_10_ema`
  - MACD: `macd`, `macds`, `macdh`
  - Momentum: `rsi`
  - Volatility: `boll`, `boll_ub`, `boll_lb`, `atr`
  - Volume: `vwma`, `mfi`

#### 3. Fundamental Data (`fundamental_data`)
- **Primary**: Alpha Vantage Fundamentals API
- **Fallback**: Yahoo Finance Financials
- **Functions**:
  - `get_fundamentals(ticker, curr_date)` - Company overview and key ratios
  - `get_balance_sheet(ticker, freq, curr_date)` - Balance sheet data
  - `get_cashflow(ticker, freq, curr_date)` - Cash flow statements
  - `get_income_statement(ticker, freq, curr_date)` - Income statements

#### 4. News and Sentiment (`news_data`)
- **Primary**: Alpha Vantage News Sentiment API
- **Fallback**: Yahoo Finance News
- **Functions**:
  - `get_news(ticker, start_date, end_date)` - Company-specific news with sentiment scores
  - `get_global_news(curr_date, look_back_days, limit)` - Global market news
  - `get_insider_sentiment(ticker, curr_date)` - Insider sentiment analysis
  - `get_insider_transactions(ticker, curr_date)` - Insider trading activity

## Configuration

### Environment Variables

Set your Alpha Vantage API key as an environment variable:

```bash
# Windows (PowerShell)
$env:ALPHA_VANTAGE_API_KEY = "your-api-key-here"

# Windows (CMD)
set ALPHA_VANTAGE_API_KEY=your-api-key-here

# Linux/Mac
export ALPHA_VANTAGE_API_KEY=your-api-key-here
```

### Getting an Alpha Vantage API Key

1. Visit [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
2. Sign up for a free API key (or premium for higher rate limits)
3. Free tier includes: 25 API requests per day, 5 API requests per minute

### Default Configuration

The project is pre-configured in `tradingagents/default_config.py`:

```python
"data_vendors": {
    "core_stock_apis": "alpha_vantage, yfinance",
    "technical_indicators": "alpha_vantage, yfinance",
    "fundamental_data": "alpha_vantage, yfinance",
    "news_data": "alpha_vantage, yfinance",
},
```

### Custom Configuration (Optional)

You can override the default configuration programmatically:

```python
from tradingagents.dataflows.config import set_config

# Use only Yahoo Finance (no Alpha Vantage)
set_config({
    "data_vendors": {
        "core_stock_apis": "yfinance",
        "technical_indicators": "yfinance",
        "fundamental_data": "yfinance",
        "news_data": "yfinance",
    }
})

# Use Alpha Vantage only (no fallback)
set_config({
    "data_vendors": {
        "core_stock_apis": "alpha_vantage",
        "technical_indicators": "alpha_vantage",
        "fundamental_data": "alpha_vantage",
        "news_data": "alpha_vantage",
    }
})
```

## Agent Integration

### Market Analyst
- **Data Sources**: Alpha Vantage Time Series + Technical Indicators, Yahoo Finance
- **Analysis**: Technical analysis with price data and indicators
- **Features**: 
  - OHLCV price data
  - Moving averages (SMA, EMA)
  - MACD indicators
  - RSI momentum
  - Bollinger Bands volatility
  - Volume analysis

### News Analyst
- **Data Sources**: Alpha Vantage News Sentiment API, Yahoo Finance News
- **Analysis**: Global news and macroeconomic analysis
- **Features**:
  - Company-specific news with sentiment scores
  - Global market news and trends
  - Macroeconomic developments
  - Sector and industry news

### Social Media Analyst
- **Data Sources**: Alpha Vantage News Sentiment API, Yahoo Finance News
- **Analysis**: Social sentiment and company-specific news
- **Features**:
  - News sentiment scores and trends
  - Public perception analysis
  - Social media discussion tracking
  - Sentiment trajectory analysis

### Fundamentals Analyst
- **Data Sources**: Alpha Vantage Fundamentals API, Yahoo Finance Financials
- **Analysis**: Deep fundamental analysis of companies
- **Features**:
  - Company overview and key ratios (P/E, P/B, ROE, etc.)
  - Balance sheet analysis
  - Cash flow analysis
  - Income statement analysis
  - Valuation metrics

## Rate Limiting and Failover

### Alpha Vantage Rate Limits
- **Free Tier**: 25 requests/day, 5 requests/minute
- **Premium**: Higher limits available

### Automatic Failover Behavior

When Alpha Vantage rate limits are exceeded:

1. The system detects `AlphaVantageRateLimitError`
2. Automatically falls back to Yahoo Finance
3. Logs the failover event
4. Continues analysis without interruption

Example log output:
```
DEBUG: Attempting PRIMARY vendor 'alpha_vantage' for get_stock_data
RATE_LIMIT: Alpha Vantage rate limit exceeded, falling back to next available vendor
DEBUG: Attempting FALLBACK vendor 'yfinance' for get_stock_data
SUCCESS: Vendor 'yfinance' succeeded
```

## API Data Quality Comparison

| Feature | Alpha Vantage | Yahoo Finance |
|---------|---------------|---------------|
| Historical Price Data | ✅ High Quality | ✅ High Quality |
| Technical Indicators | ✅ Pre-calculated | ⚠️ Requires calculation |
| Fundamental Data | ✅ Comprehensive | ✅ Good Coverage |
| News Sentiment | ✅ With scores | ⚠️ Without scores |
| Global News | ✅ Multi-topic | ✅ General market |
| Rate Limits | ⚠️ 25/day free | ✅ More generous |
| Reliability | ✅ Professional | ✅ Very reliable |
| Real-time Data | ✅ Available | ✅ Available |

## Advantages of Dual-Source Architecture

1. **Reliability**: If one API fails, the other provides backup
2. **Rate Limit Protection**: Automatic failover when limits are exceeded
3. **Data Quality**: Alpha Vantage provides professional-grade data
4. **Coverage**: Yahoo Finance provides broad market coverage
5. **Cost Efficiency**: Free tier usage optimized across both APIs

## Troubleshooting

### Alpha Vantage API Issues

**Problem**: `ALPHA_VANTAGE_API_KEY environment variable is not set`
**Solution**: Set the environment variable with your API key

**Problem**: Rate limit exceeded
**Solution**: System automatically falls back to Yahoo Finance. For more requests, upgrade to Alpha Vantage premium.

**Problem**: Invalid API key
**Solution**: Verify your API key at [Alpha Vantage Support](https://www.alphavantage.co/support/)

### Yahoo Finance Fallback Issues

**Problem**: Yahoo Finance also failing
**Solution**: Check internet connection. Both APIs require network access.

**Problem**: Data discrepancies between sources
**Solution**: This is normal. Different data providers may have slight variations. Alpha Vantage is generally more accurate.

## Best Practices

1. **Always set ALPHA_VANTAGE_API_KEY** before running the application
2. **Monitor rate limits** - free tier has 25 requests/day limit
3. **Let the system handle failover** - don't manually switch vendors
4. **Use caching** - the system caches data to reduce API calls
5. **Upgrade if needed** - for production use, consider Alpha Vantage premium tier

## Future Enhancements

Potential improvements to the API integration:

- [ ] Add caching layer for Alpha Vantage responses
- [ ] Implement request queuing for rate limit management
- [ ] Add support for additional data vendors (Polygon.io, IEX Cloud)
- [ ] Enhanced sentiment analysis with NLP processing
- [ ] Real-time streaming data support
- [ ] Historical data backfilling optimization

## Support and Resources

- **Alpha Vantage Documentation**: https://www.alphavantage.co/documentation/
- **Yahoo Finance**: Built-in with `yfinance` Python package
- **Project Issues**: Report issues via GitHub Issues
- **API Key Support**: contact@alphavantage.co

## License

The API integration follows the project's main license. Note that Alpha Vantage and Yahoo Finance have their own terms of service that must be followed.
