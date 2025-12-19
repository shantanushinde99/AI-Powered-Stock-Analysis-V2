# 📊 AI Investment Dashboard 🚀

Welcome to the **AI Investment Dashboard**, a powerful Streamlit-based platform for investors and traders! This project offers three core modules:

- 📈 **Investment Plan App**: Generate personalized investment plans with AI-driven recommendations (BUY, HOLD, SELL) based on market performance, company fundamentals, and financial news.
- 📉 **Technical Analysis App**: Analyze stock trends with candlestick charts, technical indicators (e.g., SMA, RSI), intraday data, price alerts, and multi-stock comparisons.
- 🤖 **TradingAgents Framework**: Multi-agent AI trading system that simulates a real-world trading firm with specialized LLM-powered agents working collaboratively to make informed trading decisions.

Built with Python, Streamlit, yfinance/Alpha Vantage, and LangChain, this dashboard is perfect for long-term investors and short-term traders alike. 🌟

⚠️ **Disclaimer**: This is for Educational Purposes Only - Not Recommended for Professional Uses

## 📊 Data Sources - NEW! 🆕

The dashboard now uses **Alpha Vantage API** as primary source with **Yahoo Finance** as automatic fallback:

- **🥇 Alpha Vantage** - Professional-grade data with sentiment scores (Primary)
- **🥈 Yahoo Finance** - Reliable market data, always available (Automatic Fallback)
- **🔄 Smart Failover** - Automatically switches if rate limits are exceeded
- **💰 Free Tier** - 25 Alpha Vantage requests/day included

### Quick Setup (2 minutes)
```bash
# Get free API key: https://www.alphavantage.co/support/#api-key
# Windows PowerShell:
$env:ALPHA_VANTAGE_API_KEY = "YOUR-KEY-HERE"
```

📖 **Full Documentation**:
- 🚀 [Quick Setup Guide](SETUP_GUIDE.md) - Get started in 5 minutes
- 📚 [API Integration Details](API_INTEGRATION.md) - Complete technical documentation

## 🎥 Demo Video

Watch a quick demo of the AI Investment Dashboard in action! 📽️

![Demo](https://github.com/shantanushinde99/AI-Powered-Stock-Analysis-and-CandleStick-Chart/blob/main/images/Demo1.gif?raw=true)

Full Video is there with Latest Features as well [full video](https://github.com/shantanushinde99/AI-Powered-Stock-Analysis-and-CandleStick-Chart/blob/main/Full%20Video_2.mp4)

## 🖼️ Screenshots

Here’s a glimpse of the dashboard’s sleek interface! 🖥️

| **Dashboard Landing Page** | **Technical Analysis App** |
|----------------------------|----------------------------|
| ![Dashboard](images/Screenshot(107).png) | ![Technical Analysis](images/Screenshot(108).png) |

## ✨ Features

### Investment Plan App 📈
- **AI Recommendations**: Get BUY, HOLD, SELL signals based on market data and sentiment analysis.
- **Comprehensive Reports**: Generate detailed investment plans with company overviews and ranked opportunities.
- **News Integration**: Stay informed with real-time financial news.

### Technical Analysis App 📉
- **Candlestick Charts**: Visualize stock price movements with interactive Bokeh charts.
- **Technical Indicators**: Analyze trends with SMA, EMA, RSI, MACD, and more.
- **Intraday Data**: Support for 1-hour and 30-minute intervals for precise trading.
- **Price Alerts**: Set upper/lower price thresholds with visual alerts on charts.
- **Multi-Stock Comparison**: Compare normalized price trends across multiple stocks.

### TradingAgents Framework 🤖 **NEW!**
- **Multi-Agent System**: Simulates a real-world trading firm with specialized AI agents
- **Analyst Team**: Market, Social Media, News, and Fundamentals analysts
- **Research Team**: Bull and Bear researchers with Research Manager
- **Trading Team**: Trader agent that synthesizes all insights
- **Risk Management**: Aggressive, Conservative, and Neutral risk analysts
- **Portfolio Management**: Final decision maker that approves/rejects trades
- **LLM Provider Support**: 
  - 🟢 Google (Gemini models)
  - 🔵 OpenRouter (Llama, DeepSeek models)
  - 🟣 Groq (Fast Llama inference)
- **Customizable Research Depth**: Control debate rounds and analysis thoroughness
- **Comprehensive Reports**: Detailed analysis from each agent team with final trading decision

## 🛠️ Installation

Get started in just a few steps! 🔧 Use Python 3.11 

### Basic Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/ai-investment-dashboard.git
   cd ai-investment-dashboard
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Basic Dependencies**:
   ```bash
   pip install streamlit pandas yfinance bokeh numpy TA-Lib
   ```

   *Note*: For `TA-Lib`, you may need to install the binary first:
   ```bash
   pip install TA-Lib
   ```
   If issues arise, follow the [TA-Lib installation guide](https://github.com/TA-Lib/ta-lib-python).

### TradingAgents Installation (Optional)

To use the TradingAgents Framework, follow these additional steps:

1. **Run the automated installer** (Windows):
   ```bash
   install_tradingagents.bat
   ```

   **OR install manually**:
   ```bash
   pip install -r requirements.txt
   cd TradingAgents
   pip install -r requirements.txt
   cd ..
   ```

2. **Configure API Keys**:
   - Copy `.env.example` to `.env`
   - Add your API keys (see `TRADINGAGENTS_SETUP.md` for details)

3. **Get API Keys**:
   
   **LLM Provider** (Choose at least one):
   - **Google AI** (Recommended): https://makersuite.google.com/app/apikey
   - **OpenRouter** (Alternative): https://openrouter.ai/keys
   - **Groq** (Alternative): https://console.groq.com/keys
   
   **Data Source** (Optional - for Alpha Vantage):
   - **Alpha Vantage**: https://www.alphavantage.co/support/#api-key

For detailed TradingAgents setup instructions, see:
- 📚 [Complete Setup Guide](TRADINGAGENTS_SETUP.md)
- 📋 [Quick Reference](QUICK_REFERENCE.md)
- 📝 [Implementation Summary](IMPLEMENTATION_SUMMARY.md)

## 🚀 Usage

Run the dashboard with a single command! 🏃‍♂️

```bash
streamlit run "Home Page.py"
```

- Open your browser at `http://localhost:8501`.
- Use the sidebar to select between:
  - **Investment Plan App**
  - **Technical Analysis App**
  - **TradingAgents Framework** (if configured)

### Investment Plan App
- Get AI-driven investment recommendations
- View comprehensive company analysis
- Access real-time financial news

### Technical Analysis App
- Choose S&P 500 companies
- Select a date range and data interval (`1d`, `1h`, `30m`)
- Add technical indicators and price alerts for analysis

### TradingAgents Framework 🤖
1. Scroll to the "TradingAgents Framework" section
2. Configure your API keys (or use .env file)
3. Select LLM provider (Google/OpenRouter/Groq)
4. Choose quick-thinking and deep-thinking models
5. Enter stock ticker and analysis date
6. Select analyst team members
7. Set research depth (1-5)
8. Click "Start TradingAgents Analysis"
9. Review comprehensive reports from all agent teams

**See [Quick Reference](QUICK_REFERENCE.md) for detailed usage guide.**


## 🌟 What's New

Recent updates to make your experience even better! 🎉

### Version 2.0 - TradingAgents Integration 🤖
- **Multi-Agent Trading Framework**: Complete integration of TradingAgents framework
- **LLM Provider Support**: Google (Gemini), OpenRouter (Llama), and Groq (Fast Llama)
- **Specialized AI Agents**: Analyst, Research, Trading, Risk Management, and Portfolio Management teams
- **Customizable Analysis**: Configurable research depth and agent selection
- **Comprehensive Reports**: Detailed analysis from each agent team with tabbed results
- **Environment Configuration**: Easy API key management with .env support

### Previous Updates
- **Intraday Data Support**: Analyze stocks with 1-hour or 30-minute intervals for precise trading
- **Price Alerts**: Visualize key price levels with dashed lines on candlestick charts
- **Multi-Stock Comparison**: Compare multiple stocks with normalized price trends
- **Robust Datetime Handling**: Fixed datetime issues for accurate date range filtering
- **Enhanced AI Recommendations**: Improved BUY/SELL signals with sentiment analysis

## 📚 Documentation

- 📖 **Main README**: You're reading it!
- 🚀 **Quick Reference**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- 📘 **Setup Guide**: [TRADINGAGENTS_SETUP.md](TRADINGAGENTS_SETUP.md)
- 📝 **Implementation Details**: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
- 🤖 **TradingAgents Docs**: [TradingAgents/README.md](TradingAgents/README.md)


## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. 📄

## 📬 Contact

Have questions or feedback? Reach out! ✉️

- **GitHub**: [Shantanu Shinde](https://github.com/shantanushinde99)
- **Email**: shantanushinde233@gmail.com

### TradingAgents Community

For TradingAgents-specific questions:
- **GitHub**: [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents)
- **Discord**: [Join Community](https://discord.com/invite/hk9PGKShPK)
- **Research Paper**: [arXiv:2412.20138](https://arxiv.org/abs/2412.20138)

## 🙏 Acknowledgments

- **TradingAgents Framework**: Created by [Tauric Research](https://tauric.ai/)
- **LangChain**: For LLM integration capabilities
- **Streamlit**: For the amazing web framework
- **yfinance**: For stock market data access
- **Alpha Vantage**: For fundamental and news data APIs


