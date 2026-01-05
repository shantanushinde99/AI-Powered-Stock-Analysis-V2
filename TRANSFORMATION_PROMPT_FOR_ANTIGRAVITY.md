# Complete Streamlit to FastAPI + Next.js/React Transformation Prompt

## 🎯 Project Overview
Transform this **complete Stock Trading & Analysis Platform** from a Streamlit-based application to a modern **FastAPI backend + Next.js/React frontend** architecture. This is a full-stack AI-powered trading analysis platform with 4 main modules and a sophisticated multi-agent trading framework.

---

## 📁 PROJECT STRUCTURE TO TRANSFORM

### **Current Streamlit Files:**
1. **Home Page.py** - Main TradingAgents analysis page
2. **Pages Folder:**
   - Strategy_Developer.py - Strategy development & trade logging
   - Technical_Analysis.py - Technical chart analysis
   - Candle Stick Chart.py - Advanced candlestick patterns
   - Investment_Strategist.py - AI investment strategist

### **Supporting Framework:**
- **TradingAgents/** - Custom multi-agent LLM trading framework (customized for this use case)
- **utils/data_vendor.py** - Data fetching utilities
- **strategy_data/** - JSON storage for strategies
- **eval_results/** - Trading logs and analysis results

---

## 🚀 MODULE 1: HOME PAGE - TradingAgents Analysis Engine

### **Core Functionality:**
Multi-agent AI trading analysis system that simulates a real trading firm with specialized agents collaborating to make trading decisions.

### **UI Components & Features:**

#### **1. Page Header & Configuration Section**
- **Title:** "🤖 Trading Agents"
- **Description text block:** About TradingAgents framework (markdown formatted)
- **Agent team list display:**
  - Analyst Team (Fundamentals, Sentiment, News, Technical)
  - Research Team (Bull/Bear researchers + Manager)
  - Trading Team (Trader agent)
  - Risk Management (Aggressive, Conservative, Neutral)
  - Portfolio Management (Final decision maker)

#### **2. API Keys Configuration (2-column layout)**
- **Column 1: LLM Provider Selection**
  - Dropdown: "Select LLM Provider" - Options: ["Google", "Groq"]
  - **If Google selected:**
    - Password text input: "Google API Key"
    - Environment variable setting capability
  - **If Groq selected:**
    - Password text input: "Groq API Key"
    - Environment variable setting capability
  
  - **Data Source Configuration:**
    - Dropdown: "Select Data Vendor"
      - Options: ["Yahoo Finance (yfinance)", "Alpha Vantage"]
    - **If Yahoo Finance:** Info message - "No API key required, Unlimited requests"
    - **If Alpha Vantage:**
      - Password text input: "Alpha Vantage API Key"
      - Info message about rate limits (25 requests/day, 5/minute)
      - Success/warning indicators for API key status

- **Column 2: Trading Parameters**
  - **Ticker Selection System:**
    - Categorized dropdown with 6 categories:
      1. **Major Indices:** SPY, QQQ, DIA, IWM, VTI
      2. **Tech Stocks:** AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA, NFLX
      3. **Blue Chip Stocks:** JPM, BAC, WMT, JNJ, V, MA, PG, KO
      4. **Cryptocurrencies:** BTC-USD, ETH-USD, BNB-USD, ADA-USD, SOL-USD, DOGE-USD
      5. **Forex Pairs:** EURUSD=X, GBPUSD=X, USDJPY=X, USDCAD=X, AUDUSD=X, USDCHF=X, NZDUSD=X
      6. **Commodities:** GC=F (Gold), SI=F (Silver), CL=F (Crude Oil), NG=F (Natural Gas)
    - **OR "Custom" option** with text input field
    - Display format: "Name - SYMBOL" (e.g., "Apple - AAPL")
    - Show category tag below selected ticker
  
  - **Date Range Selection (2 sub-columns):**
    - Date picker: "From Date" - Default: 30 days ago, Max: today
    - Date picker: "To Date" - Default: yesterday, Max: today
    - **Date validation:** Error message if start_date > end_date
    - **Automatic chunking for large ranges:**
      - If range > 30 days, split into monthly segments
      - Display info box showing all segments with dates
      - Show total days being analyzed
  
  - **Analyst Team Selection (2 sub-columns checkboxes):**
    - ☑ Market Analyst (default: checked)
    - ☑ Social Media Analyst (default: checked)
    - ☑ News Analyst (default: checked)
    - ☑ Fundamentals Analyst (default: checked)
  
  - **Research Depth Slider:**
    - Range: 1-5
    - Default: 1
    - Label: "Research Depth" 
    - Help text: "Number of debate rounds (1=Shallow, 5=Deep)"
  
  - **Verbose Mode Checkbox:**
    - Label: "Show Verbose Logs"
    - Default: unchecked
    - Help: "Display detailed agent communication and data fetching logs"

#### **3. Model Selection Section (2-column layout)**
- **Dynamic model dropdowns based on selected provider:**
  
  **Google Models:**
  - Quick-thinking: gemini-3-pro-preview, gemini-3-flash-preview, gemini-2.5-pro, gemini-flash-latest, gemini-flash-lite-latest, gemini-2.5-flash, gemini-2.5-flash-lite, gemini-2.0-flash, gemini-2.0-flash-lite
  - Deep-thinking: (same list)
  
  **Groq Models:**
  - Quick-thinking: llama-3.1-8b-instant, llama-3.3-70b-versatile, meta-llama/llama-4-maverick-17b-128e-instruct, meta-llama/llama-4-scout-17b-16e-instruct
  - Deep-thinking: llama-3.3-70b-versatile, meta-llama/llama-4-maverick-17b-128e-instruct, meta-llama/llama-4-scout-17b-16e-instruct, meta-llama/llama-guard-4-12b

- **Column 1:**
  - Dropdown: "Select Quick-Thinking Model"
  - Caption: "Used for fast reasoning tasks and analysis"
- **Column 2:**
  - Dropdown: "Select Deep-Thinking Model"
  - Caption: "Used for complex reasoning and decision-making"

#### **4. Run Analysis Section**
- **Validation System:**
  - Check: start_date <= end_date
  - Check: At least one analyst selected
  - Check: Required API keys present
  - Check: Valid date range
  - Display all error messages prominently

- **Primary Action Button:**
  - Label: "🚀 Start TradingAgents Analysis"
  - Type: Primary button
  - State: Disabled if validation fails
  - **On click behavior:**
    - Initialize TradingAgentsGraph with custom config
    - Configure data vendors with fallback logic
    - Show progress indicators:
      - Progress bar (0-100%)
      - Status text updates
      - If verbose mode: Expandable logs container with real-time logs
    - Process each date segment (if chunked)
    - Extract sources/URLs from all reports
    - Store results in session state

#### **5. Results Display (Multiple Sections)**

**A. Segment Overview (if multiple segments):**
- Expandable section: "View All X Time Segments Analysis"
- Shows decision for each segment with dates

**B. Executive Summary:**
- **3-column metrics:**
  - Column 1: Large recommendation display (BUY/SELL/HOLD) with color coding
  - Column 2: Analysis Period metric
  - Column 3: Ticker metric

- **3-column key insights:**
  - 🐂 Bullish Points (top 3)
  - 🐻 Bearish Points (top 3)
  - ⚠️ Key Risks (top 3)
  - Extract using NLP key point extraction

**C. Detailed Analysis Reports (5 tabs):**

**Tab 1: 📊 Analyst Reports**
- Expandable sections for each report:
  - 📈 Market Analyst Report
  - 💬 Social Media Analyst Report
  - 📰 News Analyst Report
  - 📊 Fundamentals Analyst Report
- Each shows:
  - Key insights (3-5 bullet points extracted)
  - Full report in nested expander

**Tab 2: 🔍 Research Team**
- 2-column layout:
  - Column 1: 🐂 Bull Researcher Arguments
    - Key points as success messages
    - Full case in expander
  - Column 2: 🐻 Bear Researcher Arguments
    - Key points as error messages
    - Full case in expander
- Below: 👨‍⚖️ Research Manager's Final Assessment
  - Key points as markdown
  - Full decision in expander

**Tab 3: 💼 Trading Plan**
- Display trader's investment plan
- Extract 6 key action items
- Full plan in expander

**Tab 4: ⚠️ Risk Assessment**
- 3-column layout:
  - 🔴 Aggressive View (truncated points + full analysis)
  - 🟡 Balanced View (truncated points + full analysis)
  - 🟢 Conservative View (truncated points + full analysis)

**Tab 5: ✅ Final Decision**
- Portfolio Manager's final decision
- Key decision points (5 items)
- Full rationale in expander
- **Trading Signal JSON display:**
  ```json
  {
    "ticker": "XXX",
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD",
    "segments_analyzed": N,
    "decision": "BUY/SELL/HOLD",
    "timestamp": "ISO-format"
  }
  ```
- Visual signal indicator (green BUY, red SELL, yellow HOLD)

**D. Sources & References Section:**
- 2-column layout of clickable source URLs
- Domain name extraction for display
- Total source count indicator

### **Helper Functions to Implement:**
1. `calculate_date_ranges()` - Splits large date ranges into monthly chunks
2. `format_date_range_info()` - Formats date range display text
3. `extract_key_points()` - NLP-based key point extraction (max 5 points)
4. `create_executive_summary()` - Creates summary from state data
5. URL extraction from analysis text

### **State Management:**
- Session state for `trading_analysis` with:
  - ticker, start_date, end_date
  - date_ranges (list of tuples)
  - all_segments_results
  - segment_decisions
  - final_state
  - decision
  - sources (list of URLs)
  - timestamp

---

## 🎯 MODULE 2: STRATEGY DEVELOPER & WINNING RATE

### **Core Functionality:**
Complete strategy development, trade logging, performance analytics, and AI-powered compliance checking system.

### **Session State Variables:**
- `strategy_data`: instrument, entry_rules, exit_rules, stop_loss, take_profit, strategy_description, time_window, trades[], chart_analysis
- `gemini_api_key`
- `groq_api_key`
- `rephrased_content`
- `compliance_analysis`

### **File Storage:**
- JSON files in `strategy_data/` folder
- Format: `{instrument}_strategy.json`
- Auto-save on every change

### **Sidebar Components:**
- **Groq API Key input** (password field)
- **Gemini API Key input** (password field)
- **Quick Guide section** (5-step markdown list)

### **Tab 1: 🎯 Strategy Setup**

#### **Section 1: Instrument Selection (2-column)**
- **Column 1:**
  - Text input: "Enter Instrument Name"
  - Help text: "e.g., BTC/USDT, GOLD, NIFTY, AAPL"
  - Primary button: "Load/Create Strategy"
    - If exists: Load from JSON
    - If new: Create new strategy
    - Success/error messages
  - Display current instrument with warning

- **Column 2:**
  - Text area: "Describe your trading strategy"
  - Height: 150px
  - Auto-save on change

#### **Section 2: Trading Time Window (2-column)**
- **Column 1:**
  - Dropdown with options:
    - "None - Trade Anytime"
    - "Asia Session (1:30 AM - 2:30 PM)"
    - "London Session (1:30 PM - 10:30 PM)"
    - "New York Session (5:30 PM - 2:30 AM)"
  - Auto-save on change

- **Column 2:**
  - Info box with session characteristics:
    - 🌏 Asia: Low-medium volatility
    - 🇬🇧 London: High volatility
    - 🇺🇸 New York: High volatility
  - Source link to BabyPips

#### **Section 3: Trade System Components (2-column)**
- **Column 1:**
  - Text area: "Entry Rules" (height: 150px)
  - Text area: "Stop-Loss Rules" (height: 100px)

- **Column 2:**
  - Text area: "Exit Rules" (height: 150px)
  - Text area: "Take-Profit Rules" (height: 100px)

- All auto-save on change

#### **Section 4: AI Strategy Rephrasing**
- Info message about AI functionality
- Primary button: "✨ Analyze"
- **On click:**
  - Validate: Groq API key, instrument, content
  - Call Groq API (openai/gpt-oss-120b model)
  - Show spinner during processing
  - Store in `rephrased_content` state
- **Display rephrased result:**
  - Expandable section with markdown formatted output
  - "Copy to Clipboard" button
  - "Clear" button

### **Tab 2: 📊 Trade Logging**

#### **Section 1: Quick Trade Statistics (3-column)**
- Number inputs:
  - Total Trades (calculated from logged trades)
  - Winning Trades (max: total trades)
  - Losing Trades (max: total trades)

#### **Section 2: Win Rate Metrics (3-column)**
- Metric displays:
  - Win Rate percentage
  - Risk/Reward Needed ratio
  - vs Breakeven (50%) delta

#### **Section 3: Dynamic Feedback**
- Smart feedback based on win rate:
  - <30%: Warning with improvement tips
  - 30-40%: Info with focus areas
  - 40-50%: Getting there message
  - 50-60%: Solid performance
  - 60-70%: Excellent trading
  - >70%: Elite performance
- Each with specific actionable advice

#### **Section 4: CSV Import (Expandable)**
- File uploader for CSV
- **Required columns:** Date & Time, Entry Price, Exit Price, Result
- **Optional columns:** Stop-loss, Take-profit, Notes, Strategy Name
- Show example CSV format (toggle)
- Display preview of uploaded data (first 10 rows)
- **Import modes:**
  - Append to existing trades
  - Replace all trades
- Import button with error handling
- Show import results (success count + errors)

#### **Section 5: Add New Trade (Expandable)**
- **2-column form:**
  - Column 1: trade_date, trade_time, entry_price, exit_price, stop_loss_price
  - Column 2: take_profit_price, trade_result (Win/Loss), strategy_name, trade_notes
- "Save Trade" button
- Calculate R:R ratio automatically
- Auto-save to JSON

#### **Section 6: Trade History Table**
- Display all trades in formatted DataFrame
- Columns: Date & Time, Instrument, Entry Price, Exit Price, Stop-loss, Take-profit, R:R Ratio, Result, Notes, Strategy Name
- Format dates, prices, ratios
- Height: 400px
- **Export options (3-column):**
  - "Export to CSV" download button
  - "Clear All Trades" with confirmation
  - Trade count display

#### **Section 7: AI Strategy Compliance Check**
- Info message about analysis
- "Analyze Compliance" primary button
- **On click:**
  - Validate: Gemini API key, trades exist, strategy defined
  - Call Gemini 2.5-flash model
  - Analyze last 10 trades against strategy rules
  - Return structured JSON with:
    - compliance_score (0-100)
    - overall_rating
    - metrics (7 categories with scores)
    - violations (severity: critical/warning/suggestion)
    - strengths
    - action_items
    - trade_analysis (individual trade breakdown)
  - Store in `compliance_analysis` state

#### **Section 8: Compliance Dashboard**
- **Header with metrics (4-column):**
  - Column 1: Gauge chart (Plotly) showing compliance score
  - Column 2: Status emoji (🟢/🟡/🔴) with score
  - Column 3: Critical issues count, Warnings count
  - Column 4: Strengths count, Action items count

- **Compliance Breakdown Cards:**
  - 7 metrics in 3-column grid:
    - Instrument compliance
    - Time window compliance
    - Risk management
    - Entry rules
    - Exit rules
    - Stop-loss usage
    - Take-profit usage
  - Each card shows:
    - Status emoji (✅/⚠️/❌)
    - Metric name
    - Score percentage
    - Message
    - Color-coded border/background

- **Issues & Violations:**
  - Group by severity:
    - 🚨 Critical Issues (red)
    - ⚠️ Warnings (yellow)
    - 💡 Suggestions (blue)
  - Show trade numbers affected

- **2-column section:**
  - ✅ What You're Doing Well
  - 🎯 Action Items

- **Trade-by-Trade Breakdown (Expandable):**
  - Each trade: ✅/❌ status with issues list

- **Compliance Radar Chart (Plotly):**
  - Show all 7 metrics
  - Overlay with 90% target line

- "Re-analyze" and "Clear Dashboard" buttons

### **Tab 3: 📈 Performance Analytics**

#### **Section 1: Key Performance Indicators (4-column)**
- Metrics:
  - Total Trades, Win Rate
  - Winning Trades, Losing Trades
  - Avg R:R Ratio, Profit Factor
  - Max Win Streak, Max Loss Streak

#### **Section 2: P&L Analysis (2-column)**
- **Column 1:**
  - Total P&L metric
  - Average Win metric
  - Average Loss metric
  - Win/Loss distribution pie chart (Plotly)

- **Column 2:**
  - Equity Curve line chart (Plotly)
  - Cumulative P&L over time

#### **Section 3: Strategy Consistency Analysis (2-column)**
- **Column 1:**
  - Consistency Score (0-100)
  - Rating (Excellent/Good/Fair/Poor)
  - Color-coded progress bar

- **Column 2:**
  - Factors affecting consistency (bullet list)
  - Analysis of:
    - R:R variance
    - Stop-loss usage
    - Take-profit usage
    - Overtrading detection

#### **Section 4: Risk:Reward Analysis (2-column)**
- **Column 1:**
  - R:R ratio histogram (Plotly)
  - Color by Win/Loss

- **Column 2:**
  - R:R ratio over time scatter plot (Plotly)
  - X-axis: Trade number
  - Y-axis: R:R ratio

### **Tab 4: 🤖 AI Analysis**

#### **Chart Upload & Analysis:**
- File uploader: PNG, JPG, JPEG
- **2-column display:**
  - Column 1: Show uploaded chart image
  - Column 2: "Analyze Chart with Gemini AI" button

- **On analyze:**
  - Call Gemini 2.5-flash model with comprehensive prompt
  - Analysis includes:
    1. Chart identification & context
    2. Technical indicators analysis
    3. Price action analysis
    4. Trader's execution review
    5. Strategy recommendations
    6. Market scenario assessment
    7. Overall rating & recommendations
  - Store in `chart_analysis` state

- **Display analysis:**
  - Full markdown formatted analysis
  - "Clear Analysis" button

### **Helper Functions:**
1. `save_strategy_data()` - Save to JSON
2. `load_strategy_data()` - Load from JSON
3. `rephrase_strategy_with_groq()` - Groq API call
4. `analyze_chart_with_gemini()` - Gemini vision API call
5. `analyze_strategy_compliance_with_gemini()` - Gemini compliance check
6. `display_compliance_dashboard()` - Render dashboard with Plotly
7. `calculate_win_rate()`
8. `calculate_rr_ratio()`
9. `get_dynamic_feedback()`
10. `calculate_performance_metrics()`
11. `calculate_consistency_score()`
12. `create_equity_curve()` - Plotly chart

---

## 📊 MODULE 3: TECHNICAL ANALYSIS

### **Core Functionality:**
S&P 500 stock technical analysis with multiple indicators and downloadable data.

### **Sidebar Components:**
1. **Stock Parameters:**
   - Fetch S&P 500 companies from Wikipedia
   - Dropdown: Ticker selection (format: Company Name)
   - Date inputs: Start date (default: 2019-01-01), End date (default: today)
   - Date validation

2. **Technical Analysis Parameters:**
   - ☑ Add Volume checkbox
   - **Expandable: SMA**
     - ☑ Add SMA checkbox
     - Number input: SMA Periods (1-50, default: 20)
   - **Expandable: Bollinger Bands**
     - ☑ Add Bollinger Bands checkbox
     - Number input: BB Periods (1-50, default: 20)
     - Number input: Standard Deviations (1-4, default: 2)
   - **Expandable: RSI**
     - ☑ Add RSI checkbox
     - Number input: RSI Periods (1-50, default: 20)
     - Number input: RSI Upper (50-90, default: 70)
     - Number input: RSI Lower (10-50, default: 30)

### **Main Display:**
- **Title:** "📊 Technical Analysis Dashboard (Powered by Yahoo Finance)"
- **Description:** markdown text

### **Data Preview Section (Expandable):**
- Multi-select: Columns to display
- Display DataFrame
- Download button: CSV export

### **Interactive Chart:**
- **3-row subplot (Plotly):**
  - Row 1 (50% height): Candlestick chart
    - OHLC data
    - Optional: SMA line (orange)
    - Optional: Bollinger Bands (green upper, red lower, blue middle, dashed)
  - Row 2 (20% height): Volume bars (black, color by OHLC)
  - Row 3 (30% height): RSI line (violet)
    - Horizontal lines: RSI upper (red), RSI lower (green)

- **Chart features:**
  - Shared X-axis
  - No rangeslider
  - Legend with click-to-hide
  - Title: "{Company} Technical Analysis"
  - Height: 800px

### **Functions:**
1. `get_sp500_components()` - Scrape Wikipedia with fallback
2. `load_data_yfinance()` - Fetch OHLC data
3. `calculate_indicators()` - Compute SMA, BB, RSI
4. `convert_df_to_csv()` - Export helper

---

## 📈 MODULE 4: CANDLESTICK CHART

### **Core Functionality:**
Advanced candlestick pattern detection with multiple stocks comparison, intraday intervals, and backtesting.

### **Sidebar Components:**
1. **Company Selection:**
   - Multi-select: S&P 500 companies
   - Default: ["AAPL"]
   - Format: "TICKER - Company Name"

2. **Data Interval:**
   - Dropdown: ["1d", "1h", "30m"]
   - Default: "1d"

3. **Date Range:**
   - **Adjust based on interval:**
     - If 1h/30m: Max 7 days from today
     - If 1d: Historical data allowed
   - 2-column date inputs: Start, End

4. **Display Options:**
   - ☑ Compare Multiple Stocks
   - ☑ Close Prices (disabled if multi-stock)
   - ☑ Include Volume (disabled if multi-stock)

5. **Technical Indicators:**
   - Multi-select: ["MA", "EMA", "SMA", "WMA", "RSI", "MOM", "DEMA", "TEMA"]
   - Disabled if multi-stock mode

6. **Price Alerts:**
   - Number input: Upper Price Alert
   - Number input: Lower Price Alert

### **Main Chart (Bokeh):**
- **If single stock:**
  - Candlestick: segment lines for high/low, thick segments for open/close
  - Color: Green (close > open), Red (close < open)
  - Optional: Close price line (black)
  - Optional indicators with predefined colors
  - Price alert lines (dashed)
  - Volume subplot (bars colored by OHLC)
  
- **If multi-stock:**
  - Normalized close prices (line chart)
  - Each stock: different color from COLORS array
  - Legend with company names

- **Tools:** WheelZoom, Pan, BoxZoom, Reset
- **Tooltips:** Date, OHLC values
- Height: 500px (main), 150px (volume)

### **Metrics Sections (Expandable per company):**
- **2-column layout:**
  - **Column 1: Financial Metrics**
    - P/E Ratio
    - Market Cap (in billions)
    - Dividend Yield (percentage)
  - **Column 2: Performance Metrics**
    - Cumulative Return (percentage)
    - Annualized Volatility (percentage)
    - Max Drawdown (percentage)

- **SMA Crossover Strategy:**
  - Strategy Cumulative Return metric
  - Backtest: 10/50 SMA crossover

- **Download button:** CSV export per company

### **Candlestick Patterns Table:**
- Combined patterns from all selected stocks
- Columns: Symbol, Date, Doji, Hammer, Bullish Engulfing
- Display only detected patterns (non-zero values)

### **News Section (Expandable per company):**
- Latest 5 news articles
- Format: Markdown links with title and URL

### **Functions:**
1. `get_sp500_components()` - Same as Technical Analysis
2. `load_data_yfinance()` - With interval support
3. `get_financial_metrics()` - yfinance ticker.info
4. `get_stock_news()` - yfinance ticker.news
5. `process_data()` - Calculate TA-Lib indicators (SMA, MA, EMA, WMA, RSI, MOM, DEMA, TEMA)
6. `calculate_performance_metrics()` - Cumulative return, volatility, drawdown
7. `backtest_sma_crossover()` - 10/50 SMA strategy
8. `create_chart()` - Bokeh candlestick/line chart with volume
9. TA-Lib pattern detection: CDLDOJI, CDLHAMMER, CDLENGULFING

---

## 💼 MODULE 5: INVESTMENT STRATEGIST

### **Core Functionality:**
AI-powered investment analyst team generating comprehensive reports with market analysis, company research, and stock rankings.

### **Configuration:**
- Hardcoded Google API Key (needs environment variable support)
- Three AI agents:
  1. **Market Analyst** (Gemini 1.5-flash)
  2. **Company Researcher** (Gemini 2.0-flash)
  3. **Stock Strategist** (Gemini 1.5-pro)
  4. **Team Lead** (Gemini 2.0-flash)

### **Sidebar:**
- **Title:** "Configuration"
- **Description:** markdown text
- Text input: Stock symbols (comma-separated, default: "AAPL, TSLA, GOOG")
- Password input: API Key (optional)
- Primary button: "Generate Investment Report"

### **Main Display:**
- **Title:** "📈 AI Investment Strategist"
- **Subtitle:** "Generate personalized investment reports..."

### **On Generate Report:**
1. **Market Analysis:**
   - Fetch 6-month historical data for all symbols
   - Calculate percentage change
   - Compare stock performances
   - Rank stocks by relative performance

2. **Company Research (for each symbol):**
   - Get company info (name, sector, market cap, summary)
   - Fetch latest 5 news articles
   - Summarize with AI

3. **Stock Recommendations:**
   - Combine market analysis + company data
   - Generate investment recommendations

4. **Final Report (by Team Lead):**
   - **Structured format for each stock:**
     - ## [Company Name] ([Ticker]) Analysis
     - **Sector, Market Cap**
     - **Business Overview** (2-3 lines)
     - **Fundamentals** (P/E, Revenue Growth, Debt-to-Equity, Gross Margin)
     - **Latest News Summary** (3-5 headlines)
     - **SWOT Analysis** (Strengths, Weaknesses, Opportunities, Threats)
     - **Investment Recommendation:** BUY/HOLD/SELL
     - **Rationale** (data-driven explanation)
     - **Key Monitoring Points** (3 bullets)
   
   - **Final Ranked List:**
     - Rank all stocks from least to most recommended for buying
   
   - **Disclaimer:** Standard AI-generated advice disclaimer

### **Stock Performance Chart:**
- **Title:** "📊 Stock Performance (6-Months)"
- Plotly line chart
- X-axis: Date
- Y-axis: Closing Price (USD)
- One line per stock with legend
- Template: plotly_dark
- Interactive tooltips

### **Functions:**
1. `compare_stocks()` - Fetch and compare 6-month data
2. `get_market_analysis()` - Market analyst agent call
3. `get_company_info()` - yfinance ticker.info
4. `get_company_news()` - yfinance ticker.news (latest 5)
5. `get_company_analysis()` - Company researcher agent call
6. `get_stock_recommendations()` - Stock strategist agent call
7. `get_final_investment_report()` - Team lead aggregation with specific format

---

## 🔧 TRADINGAGENTS FRAMEWORK INTEGRATION

### **Framework Overview:**
Custom multi-agent LLM framework using LangGraph for collaborative trading analysis.

### **Key Components:**

#### **1. TradingAgentsGraph Class:**
- Initialization with config dictionary
- Analyst selection (market, social, news, fundamentals)
- Debug mode support

#### **2. Configuration System (default_config.py):**
- LLM provider selection (OpenAI, Google, Groq)
- Quick-thinking LLM model
- Deep-thinking LLM model
- Backend URL configuration
- Max debate rounds (research depth)
- Max risk discussion rounds
- Data vendor configuration:
  - core_stock_apis (yfinance, alpha_vantage, local)
  - technical_indicators (yfinance, alpha_vantage, local)
  - fundamental_data (openai, alpha_vantage, local)
  - news_data (openai, alpha_vantage, google, local)

#### **3. Agent Teams:**

**Analyst Agents:**
- Market Analyst: Price, volume, technical indicators
- Social Media Analyst: Sentiment from Reddit, Twitter
- News Analyst: Financial news, macroeconomic events
- Fundamentals Analyst: Financial statements, valuation metrics

**Researcher Team:**
- Bull Researcher: Bullish case arguments
- Bear Researcher: Bearish case arguments
- Research Manager (Judge): Synthesizes debate, makes decision

**Trader Agent:**
- Synthesizes all analyst + researcher inputs
- Creates investment plan with entry/exit strategy

**Risk Management Team:**
- Aggressive Risk Analyst
- Neutral Risk Analyst
- Conservative Risk Analyst
- Risk Manager (Judge): Final risk assessment

**Portfolio Manager:**
- Reviews all inputs
- Makes final BUY/SELL/HOLD decision
- Provides reasoning

#### **4. Data Flow:**
- `.propagate(ticker, date)` method
- Returns: (full_state_dict, final_decision_string)
- State includes:
  - market_report
  - sentiment_report
  - news_report
  - fundamentals_report
  - investment_debate_state (bull_history, bear_history, judge_decision)
  - trader_investment_plan
  - risk_debate_state (risky_history, neutral_history, safe_history, judge_decision)
  - final_decision

#### **5. CLI Interface:**
- Terminal-based interactive interface
- Parameter selection screens
- Real-time progress display
- Result visualization in terminal

### **Integration Points:**
- Environment variable loading (.env support)
- API key management (OPENAI_API_KEY, GROQ_API_KEY, GOOGLE_API_KEY, ALPHA_VANTAGE_API_KEY)
- Custom config passing to graph
- Verbose logging toggle
- Multi-date segment processing

---

## 🎨 UI/UX REQUIREMENTS

### **Streamlit-Specific Features to Replicate:**

#### **1. Layout Components:**
- `st.columns()` - Multi-column layouts (support ratios like [2,1,1])
- `st.tabs()` - Tabbed interfaces
- `st.expander()` - Collapsible sections with expand/collapse
- `st.container()` - Content grouping
- `st.sidebar` - Left sidebar panel

#### **2. Input Widgets:**
- Text input (with password masking)
- Number input (min, max, step, format)
- Date input (with min/max constraints)
- Selectbox / dropdown (with format_func for display)
- Multi-select (with multiple selections)
- Checkbox (with disabled state)
- Radio buttons
- Slider (with range and labels)
- Text area (with height parameter)
- File uploader (with type restrictions)

#### **3. Display Components:**
- Success/Error/Warning/Info message boxes (color-coded)
- Metric display (with optional delta)
- Progress bar (0-100%)
- Status text (dynamic updates)
- Markdown rendering (with tables, code blocks, lists)
- JSON display (formatted)
- Code blocks (with language syntax)
- DataFrame display (with height, column selection)
- Image display (with captions)
- Download buttons (with file name, mime type)

#### **4. Interactive Features:**
- Button states (primary, disabled)
- Button confirmation patterns (click twice to confirm)
- Real-time updates during long operations
- Spinner/loading indicators with custom messages
- Session state management
- Automatic rerun on state changes
- Form submission handling

#### **5. Data Visualization:**
- Plotly charts (line, scatter, pie, histogram, gauge, radar)
- Bokeh charts (candlestick, segments, bars)
- Interactive tooltips
- Zooming, panning, reset tools
- Multiple subplots with shared axes
- Color coding (green/red for positive/negative)
- Legends with click-to-hide

#### **6. Styling & Theming:**
- Color codes:
  - Success: #00CC96 (green)
  - Error: #EF553B (red)
  - Warning: #FFC107 (yellow)
  - Info: #0066FF (blue)
  - Neutral: #666666 (gray)
- Font sizes: headers (20-24px), body (14-16px), captions (12px)
- Card-based layouts with borders and shadows
- Responsive column layouts
- Icon/emoji usage throughout
- Dark/light theme support (plotly_dark template)

#### **7. Special Behaviors:**
- Caching expensive operations (@st.cache_data)
- Auto-save on input changes
- Validation before action buttons
- Graceful error handling with user-friendly messages
- Fallback mechanisms (e.g., yfinance if Alpha Vantage fails)
- URL extraction and clickable links
- Domain name display for sources

---

## 🔌 API & BACKEND REQUIREMENTS

### **External APIs to Integrate:**

#### **1. LLM Providers:**
- **OpenAI API:**
  - Models: gpt-4o-mini, gpt-4o, o1-preview, o4-mini, gpt-4.1-mini, gpt-4.1-nano, gpt-oss-120b
  - Endpoint: https://api.openai.com/v1
  - Authentication: Bearer token

- **Google Gemini API:**
  - Models: gemini-3-pro-preview, gemini-3-flash-preview, gemini-2.5-pro, gemini-2.5-flash, gemini-2.5-flash-lite, gemini-2.0-flash, gemini-2.0-flash-lite, gemini-flash-latest, gemini-flash-lite-latest, gemini-1.5-flash, gemini-1.5-pro
  - Endpoint: https://generativelanguage.googleapis.com/v1
  - Authentication: API key
  - Vision API support for image analysis

- **Groq API:**
  - Models: llama-3.1-8b-instant, llama-3.3-70b-versatile, meta-llama/llama-4-* variants
  - Endpoint: https://api.groq.com/openai/v1
  - Authentication: API key
  - Compatible with OpenAI SDK

#### **2. Market Data Providers:**

- **Yahoo Finance (yfinance):**
  - Free, no API key required
  - Unlimited requests
  - Data: OHLC, volume, company info, news, financial metrics
  - Historical data with intervals (1m, 5m, 15m, 1h, 1d, 1wk, 1mo)
  - Support for stocks, crypto, forex, commodities

- **Alpha Vantage API:**
  - Free tier: 25 requests/day, 5/minute
  - Premium support with TradingAgents partnership: 60 requests/minute
  - Endpoint: https://www.alphavantage.co/query
  - Data: Fundamentals, news, technical indicators, company overview
  - Functions: TIME_SERIES_DAILY, OVERVIEW, NEWS_SENTIMENT, etc.

#### **3. Social Data (via TradingAgents):**
- Reddit API (praw library)
- Twitter/X scraping
- Sentiment analysis

#### **4. Web Scraping:**
- Wikipedia S&P 500 list
- User-Agent headers required
- Fallback mechanisms

### **Backend Endpoints to Create:**

#### **Authentication & Configuration:**
- POST `/api/auth/login` - User authentication
- POST `/api/auth/register` - User registration
- POST `/api/config/api-keys` - Save API keys (encrypted)
- GET `/api/config/api-keys` - Retrieve API keys

#### **TradingAgents Module:**
- POST `/api/trading-agents/analyze` - Run full analysis
  - Body: ticker, start_date, end_date, analysts[], research_depth, llm_config, data_vendor
  - Response: analysis_id
- GET `/api/trading-agents/status/{analysis_id}` - Check progress
- GET `/api/trading-agents/results/{analysis_id}` - Get results
- GET `/api/trading-agents/sources/{analysis_id}` - Get sources list

#### **Strategy Developer:**
- POST `/api/strategies` - Create/update strategy
- GET `/api/strategies/{instrument}` - Load strategy
- GET `/api/strategies` - List all strategies
- DELETE `/api/strategies/{instrument}` - Delete strategy
- POST `/api/strategies/{instrument}/trades` - Add trade
- GET `/api/strategies/{instrument}/trades` - Get trades
- DELETE `/api/strategies/{instrument}/trades` - Clear trades
- POST `/api/strategies/{instrument}/rephrase` - Groq rephrasing
- POST `/api/strategies/{instrument}/compliance` - Gemini compliance check
- POST `/api/strategies/{instrument}/chart-analysis` - Gemini chart analysis

#### **Technical Analysis:**
- GET `/api/technical/sp500` - Get S&P 500 list
- POST `/api/technical/analyze` - Get chart data
  - Body: ticker, start_date, end_date, indicators[]
  - Response: OHLC data + indicators
- GET `/api/technical/data/{ticker}` - Get raw data

#### **Candlestick Charts:**
- POST `/api/candlestick/analyze` - Multi-stock analysis
  - Body: tickers[], start_date, end_date, interval, indicators[]
  - Response: OHLC, patterns, metrics, news
- GET `/api/candlestick/patterns/{ticker}` - Get detected patterns
- GET `/api/candlestick/news/{ticker}` - Get latest news

#### **Investment Strategist:**
- POST `/api/investment/report` - Generate investment report
  - Body: tickers[], api_key (optional)
  - Response: full_report, chart_data

### **Database Schema:**

#### **Users Table:**
```sql
users (
  id: UUID PRIMARY KEY,
  email: VARCHAR UNIQUE,
  password_hash: VARCHAR,
  api_keys: JSONB ENCRYPTED,
  created_at: TIMESTAMP,
  updated_at: TIMESTAMP
)
```

#### **Strategies Table:**
```sql
strategies (
  id: UUID PRIMARY KEY,
  user_id: UUID FOREIGN KEY,
  instrument: VARCHAR,
  strategy_description: TEXT,
  entry_rules: TEXT,
  exit_rules: TEXT,
  stop_loss: TEXT,
  take_profit: TEXT,
  time_window: VARCHAR,
  chart_analysis: TEXT,
  created_at: TIMESTAMP,
  updated_at: TIMESTAMP
)
```

#### **Trades Table:**
```sql
trades (
  id: UUID PRIMARY KEY,
  strategy_id: UUID FOREIGN KEY,
  date_time: TIMESTAMP,
  instrument: VARCHAR,
  entry_price: DECIMAL,
  exit_price: DECIMAL,
  stop_loss: DECIMAL,
  take_profit: DECIMAL,
  rr_ratio: DECIMAL,
  result: VARCHAR,
  notes: TEXT,
  strategy_name: VARCHAR,
  created_at: TIMESTAMP
)
```

#### **Analyses Table:**
```sql
analyses (
  id: UUID PRIMARY KEY,
  user_id: UUID FOREIGN KEY,
  type: VARCHAR, -- 'trading_agents', 'investment_report'
  ticker: VARCHAR,
  start_date: DATE,
  end_date: DATE,
  config: JSONB,
  status: VARCHAR, -- 'pending', 'processing', 'completed', 'error'
  results: JSONB,
  sources: JSONB,
  created_at: TIMESTAMP,
  completed_at: TIMESTAMP
)
```

---

## 📦 DEPENDENCIES

### **Python Backend:**
```
fastapi
uvicorn[standard]
pydantic
python-dotenv
sqlalchemy
alembic
psycopg2-binary
redis
celery
bcrypt
python-jose[cryptography]
passlib
python-multipart
aiofiles
httpx
yfinance
pandas
numpy
plotly
ta-lib
agno
groq
google-generativeai
langchain-openai
langchain-groq
langchain-google-genai
langgraph
stockstats
praw
feedparser
chromadb
requests
lxml
html5lib
python-dateutil
typing-extensions
```

### **Next.js Frontend:**
```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "typescript": "^5.0.0",
    "@tanstack/react-query": "^5.0.0",
    "axios": "^1.0.0",
    "plotly.js": "^2.0.0",
    "react-plotly.js": "^2.0.0",
    "date-fns": "^3.0.0",
    "react-hook-form": "^7.0.0",
    "zod": "^3.0.0",
    "@hookform/resolvers": "^3.0.0",
    "tailwindcss": "^3.0.0",
    "shadcn/ui": "latest",
    "lucide-react": "latest",
    "recharts": "^2.0.0",
    "react-markdown": "^9.0.0",
    "remark-gfm": "^4.0.0",
    "papaparse": "^5.0.0",
    "file-saver": "^2.0.0"
  }
}
```

---

## 🚧 CRITICAL IMPLEMENTATION NOTES

### **1. No Data Loss:**
- All functionality must be preserved exactly
- Every button, input, display element must be replicated
- All calculations, validations, and business logic must be identical

### **2. State Management:**
- Replace st.session_state with proper React state management (Context API + React Query)
- Implement persistent storage (database + file storage)
- Handle real-time updates during long operations

### **3. Streaming & Progress:**
- Implement WebSocket or Server-Sent Events for progress updates
- Show real-time logs during TradingAgents analysis
- Progress bars must update in real-time

### **4. File Handling:**
- CSV upload with validation
- Image upload for chart analysis
- JSON download for strategies and trades
- CSV export for trade data

### **5. Authentication & Security:**
- Secure API key storage (encrypted in database)
- Environment variable management
- JWT authentication
- HTTPS only

### **6. Performance:**
- Caching for expensive API calls
- Lazy loading for large datasets
- Pagination for trade history
- Background jobs for long-running analyses (Celery + Redis)

### **7. Error Handling:**
- Graceful fallbacks (yfinance if Alpha Vantage fails)
- User-friendly error messages
- Retry mechanisms for API failures
- Validation before expensive operations

### **8. Responsive Design:**
- Mobile-friendly layouts
- Collapsible sections on mobile
- Touch-friendly controls
- Responsive charts and tables

### **9. Data Visualization:**
- Plotly.js for React (react-plotly.js)
- Bokeh equivalent: Use Plotly or Recharts
- Interactive tooltips
- Downloadable charts

### **10. Testing:**
- Unit tests for all business logic
- Integration tests for API endpoints
- E2E tests for critical user flows
- Mock external API calls in tests

---

## 📋 CHECKLIST FOR COMPLETION

### **Backend (FastAPI):**
- [ ] User authentication system (register, login, JWT)
- [ ] API key management (CRUD with encryption)
- [ ] TradingAgents integration (async analysis with progress tracking)
- [ ] Strategy CRUD operations
- [ ] Trade CRUD operations
- [ ] Compliance analysis endpoint (Gemini)
- [ ] Chart analysis endpoint (Gemini Vision)
- [ ] Strategy rephrasing endpoint (Groq)
- [ ] Technical analysis endpoints (yfinance + TA-Lib)
- [ ] Candlestick analysis endpoints (multi-stock)
- [ ] Investment report generation (AI agents)
- [ ] S&P 500 scraping endpoint
- [ ] File upload handling (CSV, images)
- [ ] CSV export generation
- [ ] WebSocket/SSE for progress updates
- [ ] Celery workers for background jobs
- [ ] Database models and migrations
- [ ] Error handling and logging
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Unit tests (>80% coverage)

### **Frontend (Next.js + React):**
- [ ] Authentication pages (login, register)
- [ ] Navigation layout with sidebar/navbar
- [ ] Home page: TradingAgents module
  - [ ] Configuration form
  - [ ] Model selection
  - [ ] Run analysis with progress
  - [ ] Executive summary display
  - [ ] 5-tab detailed reports
  - [ ] Sources section
- [ ] Strategy Developer page (4 tabs)
  - [ ] Tab 1: Strategy setup
  - [ ] Tab 2: Trade logging + compliance
  - [ ] Tab 3: Performance analytics
  - [ ] Tab 4: Chart analysis
- [ ] Technical Analysis page
  - [ ] Sidebar controls
  - [ ] Interactive Plotly charts
  - [ ] Data preview and export
- [ ] Candlestick Chart page
  - [ ] Multi-stock comparison
  - [ ] Pattern detection table
  - [ ] Metrics and news
- [ ] Investment Strategist page
  - [ ] Stock input and configuration
  - [ ] AI report generation
  - [ ] Performance chart
- [ ] Reusable components:
  - [ ] Form inputs (text, number, date, select, etc.)
  - [ ] Metric cards
  - [ ] Charts (Plotly, Recharts)
  - [ ] Data tables
  - [ ] File uploaders
  - [ ] Progress indicators
  - [ ] Message boxes (success, error, warning, info)
  - [ ] Expandable sections
  - [ ] Tabs component
  - [ ] Modal dialogs
- [ ] State management (Context + React Query)
- [ ] API integration (axios + react-query)
- [ ] Error boundary and error handling
- [ ] Loading states and skeletons
- [ ] Responsive design (Tailwind CSS)
- [ ] Dark mode support
- [ ] E2E tests (Cypress/Playwright)

### **Integration & Deployment:**
- [ ] Environment variables setup
- [ ] Database setup and migrations
- [ ] Redis setup for Celery
- [ ] Docker containerization (backend, frontend, celery, redis, postgres)
- [ ] Docker Compose for local development
- [ ] CI/CD pipeline
- [ ] Production deployment instructions
- [ ] Monitoring and logging
- [ ] Backup strategy for database

### **Documentation:**
- [ ] API documentation (Swagger)
- [ ] Frontend component documentation (Storybook)
- [ ] Setup instructions (README)
- [ ] Environment variables documentation
- [ ] Deployment guide
- [ ] User guide/tutorials

---

## 🎯 SUCCESS CRITERIA

The transformation is complete when:

1. ✅ **Every feature from Streamlit app is working in Next.js/React**
2. ✅ **No UI element is missing** (buttons, inputs, displays, charts)
3. ✅ **All calculations produce identical results**
4. ✅ **TradingAgents framework fully integrated**
5. ✅ **All 4 modules (5 pages) functional**
6. ✅ **File upload/download working**
7. ✅ **Real-time progress updates during analysis**
8. ✅ **Compliance dashboard with all visualizations**
9. ✅ **Charts are interactive and match Streamlit versions**
10. ✅ **Authentication and API key management secure**
11. ✅ **Responsive design works on all screen sizes**
12. ✅ **Error handling graceful and user-friendly**
13. ✅ **Performance optimized** (caching, lazy loading, background jobs)
14. ✅ **Tests passing** (unit, integration, E2E)
15. ✅ **Documentation complete**

---

## 💡 ADDITIONAL NOTES

- **Preserve all helper functions** and port their logic exactly
- **Maintain all validation rules** from Streamlit version
- **Keep all default values** for inputs
- **Replicate all color codes** for consistency
- **Use same terminology** (labels, help text, messages)
- **Match layout proportions** (column ratios, heights, spacing)
- **Implement same auto-save behavior** where present
- **Support same file formats** (CSV structure, JSON schema)
- **Use environment variables** for all API keys (never hardcode)
- **Implement proper logging** for debugging and monitoring
- **Add rate limiting** to prevent API abuse
- **Handle timezone conversions** properly for date inputs
- **Support data export** in same formats as Streamlit
- **Replicate warning/info messages** exactly
- **Implement same keyboard shortcuts** if any exist
- **Match loading messages** and spinner text
- **Use same emoji/icons** throughout interface

This prompt covers **100% of the functionality** in your Streamlit application. Every button, input, chart, calculation, API call, and display element has been documented in detail. Use this as your complete specification for the transformation to FastAPI + Next.js/React.

Good luck with the transformation! 🚀
