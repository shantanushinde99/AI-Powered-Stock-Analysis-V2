# 📊 AI-Powered Stock Analysis Platform

A comprehensive AI-powered investment analysis platform built with Streamlit that combines multi-agent LLM trading frameworks, technical analysis tools, and AI-driven investment strategies. This platform integrates the **TradingAgents** framework to provide collaborative, multi-agent market analysis and trading decision support.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Project Architecture](#-project-architecture)
- [TradingAgents Framework](#-tradingagents-framework)
- [Streamlit Pages](#-streamlit-pages)
- [File Structure](#-file-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Data Sources](#-data-sources)
- [API Requirements](#-api-requirements)
- [Dependencies](#-dependencies)
- [Research & Citation](#-research--citation)
- [Disclaimer](#-disclaimer)

---

## 🎯 Overview

This project is an AI-powered stock analysis platform that leverages multiple Large Language Model (LLM) agents to analyze financial markets, generate trading recommendations, and provide comprehensive investment insights. The platform is built using Streamlit for the web interface and integrates the **TradingAgents** framework, a research-grade multi-agent trading system that mirrors real-world trading firm dynamics.

### Key Capabilities

- **Multi-Agent Trading Analysis**: Uses specialized LLM-powered agents (analysts, researchers, traders, risk managers) that collaborate to evaluate market conditions
- **Technical Analysis**: Interactive candlestick charts with multiple technical indicators (SMA, EMA, RSI, Bollinger Bands, MACD, etc.)
- **AI Investment Strategist**: LLM-powered agents for company research, market analysis, and stock recommendations
- **Strategy Development**: Create, track, and analyze custom trading strategies with AI-powered compliance checking
- **Multi-Asset Support**: Stocks, ETFs, Cryptocurrencies, and Forex pairs
- **Multiple LLM Providers**: Support for Google Gemini, Groq, and OpenRouter

---

## ✨ Features

### 🤖 Multi-Agent Trading System
- Analyst teams (Fundamentals, Sentiment, News, Technical)
- Bull/Bear researcher debates
- Trader agent for strategy synthesis
- Risk management with multiple risk profiles (Aggressive, Neutral, Conservative)
- Portfolio manager for final decision making

### 📈 Technical Analysis Tools
- Interactive candlestick charts with Bokeh
- Multiple technical indicators via TA-Lib
- Pattern recognition (Doji, Hammer, Engulfing patterns)
- Performance metrics (Cumulative Return, Volatility, Max Drawdown)
- SMA Crossover backtesting

### 🧠 AI-Powered Insights
- Company profile and financial analysis
- News sentiment analysis
- SWOT analysis generation
- Investment recommendations (BUY/HOLD/SELL)
- Strategy compliance checking with Gemini AI

### 📊 Data Integration
- Yahoo Finance (yfinance) - Free, no API key required
- Alpha Vantage - Premium data with fallback support
- Real-time and historical data support
- S&P 500 component fetching

---

## 🏗 Project Architecture

```
Stock Project/
├── Home Page.py                 # Main entry point - TradingAgents UI
├── Trading Agent.py             # Alternative TradingAgents interface
├── pages/                       # Streamlit multi-page app modules
│   ├── Technical_Analysis.py    # Technical indicators and charting
│   ├── Investment_Strategist.py # AI investment analysis
│   ├── Strategy_Developer.py    # Strategy creation and tracking
│   └── Candle Stick Chart.py    # Interactive candlestick charts
├── TradingAgents/               # Multi-agent trading framework
│   └── tradingagents/           # Core library
│       ├── agents/              # All agent implementations
│       ├── dataflows/           # Data fetching and processing
│       ├── graph/               # LangGraph-based workflow
│       └── default_config.py    # Framework configuration
├── utils/                       # Utility modules
│   └── data_vendor.py           # Unified data fetching interface
├── strategy_data/               # Saved trading strategies (JSON)
├── eval_results/                # Evaluation results
├── requirements.txt             # Python dependencies
└── .env.example                 # Environment variables template
```

---

## 🤖 TradingAgents Framework

The TradingAgents framework is a sophisticated multi-agent system built with LangGraph that simulates the dynamics of a real-world trading firm. It decomposes complex trading tasks into specialized roles for robust market analysis.

### Agent Teams

#### 1. Analyst Team
The analyst team consists of four specialized agents that gather and analyze different types of market information:

| Agent | File | Purpose |
|-------|------|---------|
| **Fundamentals Analyst** | `agents/analysts/fundamentals_analyst.py` | Evaluates company financials, performance metrics, balance sheets, cash flows, and income statements to identify intrinsic value |
| **Sentiment Analyst** | `agents/analysts/social_media_analyst.py` | Analyzes social media (Reddit) and public sentiment using sentiment scoring to gauge short-term market mood |
| **News Analyst** | `agents/analysts/news_analyst.py` | Monitors global news and macroeconomic indicators, interpreting impact on market conditions |
| **Market/Technical Analyst** | `agents/analysts/market_analyst.py` | Utilizes technical indicators (MACD, RSI, SMA, etc.) to detect trading patterns and forecast price movements |

#### 2. Research Team
Researchers critically assess analyst insights through structured debates:

| Agent | File | Purpose |
|-------|------|---------|
| **Bull Researcher** | `agents/researchers/bull_researcher.py` | Presents bullish arguments and investment opportunities |
| **Bear Researcher** | `agents/researchers/bear_researcher.py` | Presents bearish arguments, risks, and potential downsides |
| **Research Manager** | `agents/managers/research_manager.py` | Moderates debates and synthesizes final research conclusions |

#### 3. Trader Agent
| Agent | File | Purpose |
|-------|------|---------|
| **Trader** | `agents/trader/trader.py` | Composes reports from analysts and researchers to create actionable trading plans with timing and position sizing |

#### 4. Risk Management Team
Multi-perspective risk assessment with three distinct viewpoints:

| Agent | File | Purpose |
|-------|------|---------|
| **Aggressive Analyst** | `agents/risk_mgmt/aggresive_debator.py` | Evaluates from a high-risk-tolerance perspective |
| **Conservative Analyst** | `agents/risk_mgmt/conservative_debator.py` | Evaluates from a risk-averse perspective |
| **Neutral Analyst** | `agents/risk_mgmt/neutral_debator.py` | Provides balanced risk assessment |
| **Risk Manager** | `agents/managers/risk_manager.py` | Final portfolio decision maker (approves/rejects trades) |

### Dataflows Module

The dataflows module (`TradingAgents/tradingagents/dataflows/`) handles all data fetching and processing:

| File | Purpose |
|------|---------|
| `interface.py` | Unified data interface for all data sources |
| `y_finance.py` | Yahoo Finance data integration (stock data, fundamentals, news) |
| `alpha_vantage_stock.py` | Alpha Vantage stock price data |
| `alpha_vantage_indicator.py` | Alpha Vantage technical indicators |
| `alpha_vantage_fundamentals.py` | Alpha Vantage fundamental data |
| `alpha_vantage_news.py` | Alpha Vantage news data |
| `reddit_utils.py` | Reddit sentiment data via PRAW |
| `googlenews_utils.py` | Google News integration |
| `stockstats_utils.py` | Technical indicator calculations |
| `yfin_utils.py` | Yahoo Finance utility functions |

### Graph Module

The graph module (`TradingAgents/tradingagents/graph/`) orchestrates the multi-agent workflow:

| File | Purpose |
|------|---------|
| `trading_graph.py` | Main TradingAgentsGraph class - entry point for analysis |
| `setup.py` | Graph node and edge configuration |
| `propagation.py` | Workflow propagation logic |
| `conditional_logic.py` | Conditional branching in workflow |
| `reflection.py` | Agent reflection and self-improvement |
| `signal_processing.py` | Final signal generation |

### Configuration

The framework is configured via `default_config.py`:

```python
DEFAULT_CONFIG = {
    # LLM Settings
    "llm_provider": "openrouter",  # Options: google, groq, openrouter
    "deep_think_llm": "deepseek/deepseek-chat-v3-0324:free",
    "quick_think_llm": "meta-llama/llama-3.3-8b-instruct:free",
    
    # Debate Settings
    "max_debate_rounds": 1,        # Bull vs Bear debate rounds
    "max_risk_discuss_rounds": 1,  # Risk team discussion rounds
    
    # Data Vendor Configuration
    "data_vendors": {
        "core_stock_apis": "alpha_vantage, yfinance",
        "technical_indicators": "alpha_vantage, yfinance",
        "fundamental_data": "alpha_vantage, yfinance",
        "news_data": "alpha_vantage, yfinance",
    }
}
```

---

## 📄 Streamlit Pages

### 1. Home Page (`Home Page.py`) - Main Trading Agents Interface

The primary interface for the TradingAgents framework featuring:

- **Configuration Panel**: LLM provider selection (Google/Groq), API key inputs, data vendor selection
- **Trading Parameters**: 
  - Pre-populated ticker lists (Major Indices, Tech Stocks, Blue Chip, Crypto, Forex, Commodities)
  - Date range selection with automatic chunking for large ranges
  - Analyst team selection (Market, Social, News, Fundamentals)
  - Research depth slider (1-5 debate rounds)
- **Model Selection**: Quick-thinking and Deep-thinking model selection
- **Results Display**:
  - Executive summary with BUY/SELL/HOLD recommendations
  - Key bullish/bearish points and risks
  - Detailed analyst reports
  - Research team debate history
  - Trading plan
  - Risk assessment from multiple perspectives
  - Source citations

**Key Functions:**
- `calculate_date_ranges()` - Splits large date ranges into monthly chunks
- `extract_key_points()` - Extracts actionable insights from analysis text
- `create_executive_summary()` - Creates concise summary from full analysis

### 2. Trading Agent (`Trading Agent.py`)

Alternative interface for TradingAgents with:
- Support for OpenRouter as additional LLM provider
- Simplified single-date analysis
- Embedded framework documentation viewer
- Same agent team configuration as Home Page

### 3. Technical Analysis (`pages/Technical_Analysis.py`)

Interactive technical analysis dashboard:

- **Data Source**: Yahoo Finance with S&P 500 component list
- **Technical Indicators**:
  - SMA (Simple Moving Average)
  - Bollinger Bands (with configurable periods and standard deviations)
  - RSI (Relative Strength Index) with overbought/oversold lines
  - Volume overlay
- **Features**:
  - Interactive Plotly charts
  - Customizable indicator parameters
  - CSV data export
  - Date range selection

### 4. Investment Strategist (`pages/Investment_Strategist.py`)

AI-powered investment analysis using the Agno framework with Google Gemini:

**Agent Architecture:**
| Agent | Model | Role |
|-------|-------|------|
| Market Analyst | gemini-1.5-flash | Analyzes and compares stock performance over 6 months |
| Company Researcher | gemini-2.0-flash | Fetches company profiles, financials, and news |
| Stock Strategist | gemini-1.5-pro | Provides investment insights and recommendations |
| Team Lead | gemini-2.0-flash | Aggregates all analysis into final investor report |

**Output Format:**
- Business overview and sector analysis
- Fundamental metrics (P/E, Revenue Growth, Debt-to-Equity)
- SWOT analysis
- Investment recommendation with rationale
- Ranked stock list
- Interactive 6-month performance chart

### 5. Strategy Developer (`pages/Strategy_Developer.py`)

Comprehensive trading strategy management tool with four tabs:

**Tab 1: Strategy Setup**
- Instrument selection with validation
- Strategy description with AI grammar correction (Groq)
- Trading session/time window selection
- Entry/exit rules definition
- Stop-loss and take-profit rules

**Tab 2: Trade Logging**
- Manual trade entry with all fields
- Trade history viewer
- CSV import/export

**Tab 3: Performance Analytics**
- Win rate calculations
- Equity curve visualization
- Risk:Reward ratio analysis
- Consistency scoring
- Dynamic AI feedback based on performance

**Tab 4: AI Analysis**
- Chart analysis with Gemini vision models
- Strategy compliance checking
- Detailed compliance dashboard with violations

**Key Functions:**
- `rephrase_strategy_with_groq()` - Grammar correction for strategy descriptions
- `analyze_chart_with_gemini()` - Vision-based chart analysis
- `analyze_strategy_compliance_with_gemini()` - JSON-structured compliance checking
- `display_compliance_dashboard()` - Visual compliance reporting

### 6. Candlestick Chart (`pages/Candle Stick Chart.py`)

Advanced candlestick charting with Bokeh:

- **Multi-Stock Comparison**: Normalized price comparison across multiple tickers
- **Technical Indicators**: SMA, EMA, WMA, RSI, MOM, DEMA, TEMA, MA
- **Candlestick Patterns**: Doji, Hammer, Bullish Engulfing detection via TA-Lib
- **Financial Metrics**: P/E Ratio, Market Cap, Dividend Yield
- **Performance Metrics**: Cumulative Return, Annualized Volatility, Max Drawdown
- **Backtesting**: SMA Crossover strategy backtest
- **Price Alerts**: Configurable upper/lower price alert lines
- **Data Intervals**: Daily, Hourly, 30-minute
- **News Integration**: Latest 5 news articles per stock

---

## 📁 File Structure Details

### Root Directory Files

| File | Description |
|------|-------------|
| `Home Page.py` | Main Streamlit entry point with TradingAgents integration |
| `Trading Agent.py` | Alternative TradingAgents interface with OpenRouter support |
| `fetch_tickers.py` | Asset ticker fetcher utility for stocks, crypto, and forex |
| `paper_trading.py` | Paper trading simulation data generator |
| `Tickers.py` | Ticker symbol utilities |
| `example.py` | Example usage scripts |
| `requirements.txt` | Python package dependencies |
| `requirements2.txt` | Additional dependencies |
| `.env.example` | Environment variables template |
| `Trade_logs.csv` | Sample trade log data |

### Utility Files

| File | Path | Description |
|------|------|-------------|
| `data_vendor.py` | `utils/` | Unified data vendor interface supporting Yahoo Finance and Alpha Vantage with automatic fallback |

**Key Functions in `data_vendor.py`:**
- `get_data_vendor_selection()` - Streamlit UI for vendor selection
- `fetch_stock_data()` - Unified data fetching from any vendor
- `get_current_price()` - Latest price fetcher

### Strategy Data

The `strategy_data/` directory stores JSON files for each trading strategy:
- `BTC-USD_strategy.json`
- `ETHEREUM_strategy.json`
- `BITCOIN_strategy.json`

Each file contains:
- Instrument information
- Strategy description
- Entry/exit rules
- Stop-loss/take-profit rules
- Trading time window
- Trade history

---

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager
- TA-Lib (requires separate installation)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd "Stock Project/Stock Project"
```

### Step 2: Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # macOS/Linux
```

### Step 3: Install TA-Lib

TA-Lib requires a separate installation:

**Windows:**
Download the appropriate `.whl` file from [TA-Lib Windows binaries](https://github.com/cgohlke/talib-build/releases) and install:
```bash
pip install TA_Lib-0.4.28-cp310-cp310-win_amd64.whl
```

**macOS:**
```bash
brew install ta-lib
pip install TA-Lib
```

**Linux:**
```bash
sudo apt-get install ta-lib
pip install TA-Lib
```

### Step 4: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Install TradingAgents

```bash
# Option 1: Use the provided batch file (Windows)
install_tradingagents.bat

# Option 2: Manual installation
cd TradingAgents
pip install -e .
cd ..
```

### Step 6: Configure Environment Variables

```bash
cp .env.example .env
# Edit .env with your API keys
```

---

## ⚙ Configuration

### Environment Variables

Create a `.env` file in the project root with the following:

```env
# LLM Provider API Keys (choose one or more)
GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key
OPENROUTER_API_KEY=your_openrouter_api_key

# Data Provider API Keys (optional)
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
```

### API Key Sources

| Provider | Free Tier | Get API Key |
|----------|-----------|-------------|
| Google AI | Generous free tier | [Google AI Studio](https://makersuite.google.com/app/apikey) |
| Groq | Free with rate limits | [Groq Console](https://console.groq.com/keys) |
| OpenRouter | Pay-per-use | [OpenRouter](https://openrouter.ai/keys) |
| Alpha Vantage | 25 req/day free | [Alpha Vantage](https://www.alphavantage.co/support/#api-key) |

---

## 🎮 Usage

### Running the Application

```bash
# Start the main Streamlit app
streamlit run "Home Page.py"
```

The application will open in your default browser at `http://localhost:8501`.

### Navigation

Use the sidebar to navigate between pages:
- **Home Page**: Main TradingAgents analysis
- **Technical Analysis**: Chart with indicators
- **Investment Strategist**: AI-powered stock research
- **Strategy Developer**: Custom strategy management
- **Candlestick Chart**: Advanced charting

### Quick Start Guide

1. **Select LLM Provider**: Choose Google or Groq
2. **Enter API Key**: Input your API key
3. **Choose Stock**: Select from dropdown or enter custom ticker
4. **Set Date Range**: Select analysis period
5. **Configure Analysts**: Enable/disable analyst types
6. **Run Analysis**: Click "Start TradingAgents Analysis"
7. **Review Results**: Examine the executive summary and detailed reports

---

## 📊 Data Sources

### Yahoo Finance (yfinance)
- **Cost**: Free
- **Rate Limits**: None
- **Data Types**: OHLCV, fundamentals, news, options
- **Best For**: Most use cases, unlimited requests

### Alpha Vantage
- **Cost**: Free tier (25 req/day) / Premium available
- **Rate Limits**: 5 req/min (free), 60 req/min (TradingAgents partner)
- **Data Types**: Premium fundamentals, news, technical indicators
- **Best For**: Detailed fundamental analysis

### Data Fallback System

The platform implements intelligent fallback:
1. Primary source fails → Automatically tries secondary
2. Alpha Vantage rate limit → Falls back to Yahoo Finance
3. Configurable per data category in `default_config.py`

---

## 🔑 API Requirements

### Required

| API | Purpose | Required For |
|-----|---------|--------------|
| Google API Key **OR** | LLM analysis | Core functionality |
| Groq API Key | LLM analysis | Core functionality |

### Optional

| API | Purpose | Benefit |
|-----|---------|---------|
| Alpha Vantage | Premium data | Higher quality fundamentals |
| OpenRouter | Multi-model access | Access to additional models |

---

## 📦 Dependencies

### Core Dependencies

```
streamlit          # Web application framework
yfinance          # Yahoo Finance data
pandas            # Data manipulation
numpy             # Numerical computing
plotly            # Interactive charts
bokeh             # Advanced charting
```

### AI/ML Dependencies

```
langchain-openai       # OpenAI LangChain integration
langchain-google-genai # Google AI LangChain integration
langchain-groq         # Groq LangChain integration
langgraph              # Multi-agent workflow orchestration
chromadb               # Vector database
agno                   # Agent framework
```

### Technical Analysis

```
TA-Lib            # Technical indicators (requires separate install)
pandas-ta         # Additional technical indicators
stockstats        # Stock statistics
```

### Data & Utilities

```
requests          # HTTP requests
praw              # Reddit API
feedparser        # RSS/news feeds
python-dotenv     # Environment variables
```

---

## 📚 Research & Citation

This project integrates the TradingAgents framework from Tauric Research. If you use this work in academic research, please cite:

```bibtex
@misc{xiao2025tradingagentsmultiagentsllmfinancial,
      title={TradingAgents: Multi-Agents LLM Financial Trading Framework}, 
      author={Yijia Xiao and Edward Sun and Di Luo and Wei Wang},
      year={2025},
      eprint={2412.20138},
      archivePrefix={arXiv},
      primaryClass={q-fin.TR},
      url={https://arxiv.org/abs/2412.20138}, 
}
```

**Related Links:**
- [TradingAgents Paper (arXiv)](https://arxiv.org/abs/2412.20138)
- [Tauric Research](https://tauric.ai/)
- [TradingAgents GitHub](https://github.com/TauricResearch/TradingAgents)

---

## ⚠️ Disclaimer

> **IMPORTANT**: This platform is designed for **research and educational purposes only**.

- This is **NOT** financial, investment, or trading advice
- Trading performance may vary based on:
  - Chosen LLM models and temperature settings
  - Trading periods and market conditions
  - Quality of data sources
  - Non-deterministic factors in LLM responses
- Past performance does not guarantee future results
- Always consult a licensed financial advisor before making investment decisions
- The creators assume no liability for any financial losses

---

## 📄 License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

---

**Built with ❤️ using Streamlit, LangGraph, and the power of Multi-Agent LLMs**
