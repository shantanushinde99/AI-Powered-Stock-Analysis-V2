# Quick Setup Guide - Alpha Vantage & Yahoo Finance Integration

## 🚀 Quick Start (5 Minutes)

### Step 1: Get Your Alpha Vantage API Key (2 minutes)

1. Visit: https://www.alphavantage.co/support/#api-key
2. Enter your email and click "GET FREE API KEY"
3. Copy your API key (looks like: `ABCD1234EFGH5678`)

### Step 2: Set Environment Variable (1 minute)

**Windows PowerShell:**
```powershell
$env:ALPHA_VANTAGE_API_KEY = "YOUR-API-KEY-HERE"
```

**Windows CMD:**
```cmd
set ALPHA_VANTAGE_API_KEY=YOUR-API-KEY-HERE
```

**Linux/Mac:**
```bash
export ALPHA_VANTAGE_API_KEY=YOUR-API-KEY-HERE
```

**Make it Permanent (Windows):**
```powershell
[System.Environment]::SetEnvironmentVariable('ALPHA_VANTAGE_API_KEY', 'YOUR-API-KEY-HERE', 'User')
```

### Step 3: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

Key packages installed:
- `yfinance` - Yahoo Finance API
- `requests` - For Alpha Vantage API calls
- `pandas` - Data processing
- `stockstats` - Technical indicators

### Step 4: Verify Installation (1 minute)

Run this Python snippet to test:

```python
import os
from tradingagents.dataflows.alpha_vantage_stock import get_stock
from tradingagents.dataflows.y_finance import get_YFin_data_online

# Check API key
api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
print(f"✓ API Key set: {api_key[:8]}..." if api_key else "✗ API Key missing!")

# Test Alpha Vantage (if key is set)
if api_key:
    try:
        data = get_stock("AAPL", "2024-01-01", "2024-01-05")
        print("✓ Alpha Vantage working!")
    except Exception as e:
        print(f"✗ Alpha Vantage error: {e}")

# Test Yahoo Finance (always works)
try:
    data = get_YFin_data_online("AAPL", "2024-01-01", "2024-01-05")
    print("✓ Yahoo Finance working!")
except Exception as e:
    print(f"✗ Yahoo Finance error: {e}")
```

## 🎯 What You Get

### All Agents Now Use Alpha Vantage + Yahoo Finance

✅ **Market Analyst** - Stock prices + Technical indicators  
✅ **News Analyst** - Global news with sentiment scores  
✅ **Social Media Analyst** - Sentiment analysis  
✅ **Fundamentals Analyst** - Financial statements + Ratios  

### Automatic Failover

```
Alpha Vantage (Primary) → Yahoo Finance (Fallback)
        ↓                         ↓
   Rate Limited?              Always Available
   No API Key?               Free & Reliable
        ↓                         ↓
   Auto switches to Yahoo Finance
```

## 📊 API Comparison

| Feature | Alpha Vantage (Primary) | Yahoo Finance (Fallback) |
|---------|------------------------|--------------------------|
| Price Data | ✅ Professional Grade | ✅ High Quality |
| Indicators | ✅ Pre-calculated | ✅ Calculated on-demand |
| News | ✅ With Sentiment Scores | ✅ Basic news |
| Fundamentals | ✅ Comprehensive | ✅ Good coverage |
| Rate Limit | 25/day (free) | Much higher |
| Setup | Requires API key | No setup needed |

## 🔧 Configuration (Optional)

Default config is already set in `TradingAgents/tradingagents/default_config.py`:

```python
"data_vendors": {
    "core_stock_apis": "alpha_vantage, yfinance",      # Stock prices
    "technical_indicators": "alpha_vantage, yfinance", # Technical analysis
    "fundamental_data": "alpha_vantage, yfinance",     # Financials
    "news_data": "alpha_vantage, yfinance",            # News & sentiment
}
```

**No changes needed!** The system is pre-configured for optimal performance.

## 🚨 Troubleshooting

### Problem: "API key not set" error
**Solution:** Run the environment variable command again in the same terminal/session

### Problem: Alpha Vantage rate limit (25 requests/day)
**Solution:** System automatically uses Yahoo Finance. No action needed!

### Problem: Want more API calls?
**Solution:** Upgrade to Alpha Vantage Premium: https://www.alphavantage.co/premium/

### Problem: Want to use only Yahoo Finance?
**Solution:** Just don't set the API key. System will auto-use Yahoo Finance.

## 📚 What Changed?

### Before (Old System)
- ❌ Only Yahoo Finance
- ❌ No sentiment scores
- ❌ Basic news data
- ❌ Limited indicators

### After (New System)
- ✅ Alpha Vantage + Yahoo Finance
- ✅ News with sentiment scores
- ✅ Professional-grade data
- ✅ Comprehensive indicators
- ✅ Automatic failover
- ✅ Better reliability

## 🎓 Usage Examples

### Example 1: Run Market Analysis
```python
from tradingagents.graph.trading_graph import create_trading_graph

graph = create_trading_graph(llm)
result = graph.invoke({
    "company_of_interest": "AAPL",
    "trade_date": "2024-12-01"
})
```

**What happens:**
1. Market Analyst calls Alpha Vantage for AAPL data
2. If rate limited → automatically uses Yahoo Finance
3. Gets technical indicators from best available source
4. Generates comprehensive analysis report

### Example 2: Direct API Call
```python
from tradingagents.agents.utils.core_stock_tools import get_stock_data

# This automatically tries Alpha Vantage first, then Yahoo Finance
data = get_stock_data(
    symbol="TSLA",
    start_date="2024-11-01",
    end_date="2024-12-01"
)
print(data)
```

### Example 3: Get News with Sentiment
```python
from tradingagents.agents.utils.news_data_tools import get_news

# Alpha Vantage returns news WITH sentiment scores
news = get_news(
    ticker="NVDA",
    start_date="2024-11-01",
    end_date="2024-12-01"
)
print(news)
```

## 📖 Next Steps

1. ✅ Set up API key (done above)
2. ✅ Verify installation (done above)
3. 📖 Read full documentation: [`API_INTEGRATION.md`](./API_INTEGRATION.md)
4. 🚀 Start analyzing stocks!

## 💡 Pro Tips

1. **Free Tier Optimization**: The system intelligently caches data to minimize API calls
2. **Rate Limit Strategy**: Morning analysis uses Alpha Vantage, afternoon uses cached/Yahoo data
3. **Best Data Quality**: Alpha Vantage has more accurate sentiment scores than Yahoo
4. **No Maintenance**: Failover is fully automatic - you never need to manually switch

## 🆘 Need Help?

- **Full Documentation**: See `API_INTEGRATION.md` in project root
- **Alpha Vantage Docs**: https://www.alphavantage.co/documentation/
- **Yahoo Finance Package**: https://pypi.org/project/yfinance/
- **Project Issues**: Open a GitHub issue

---

**That's it! You're ready to go! 🎉**

The system will automatically use the best available data source for every request.
