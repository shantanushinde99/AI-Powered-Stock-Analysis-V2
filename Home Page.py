import streamlit as st
import os
import sys
import io
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from contextlib import redirect_stdout, redirect_stderr

# Add TradingAgents to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'TradingAgents'))

# Set page config
st.set_page_config(
    # page_title="📊 AI Investment Dashboard",
    # page_icon="📈",
    layout="wide"
)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_date_ranges(start_date, end_date, max_days=30):
    """
    Split a date range into smaller chunks to avoid exceeding LLM context limits.
    Default chunk size is ~30 days (1 month).
    
    Args:
        start_date: Starting date (datetime.date or datetime.datetime)
        end_date: Ending date (datetime.date or datetime.datetime)
        max_days: Maximum days per chunk (default: 30)
    
    Returns:
        List of tuples containing (chunk_start_date, chunk_end_date)
    """
    # Convert to date objects if datetime
    if isinstance(start_date, datetime):
        start_date = start_date.date()
    if isinstance(end_date, datetime):
        end_date = end_date.date()
    
    date_ranges = []
    current_start = start_date
    
    while current_start < end_date:
        # Calculate chunk end (approximately 1 month)
        chunk_end = current_start + relativedelta(months=1)
        
        # Don't exceed the final end date
        if chunk_end > end_date:
            chunk_end = end_date
        
        date_ranges.append((current_start, chunk_end))
        
        # Move to next chunk (start from where we ended)
        current_start = chunk_end + timedelta(days=1)
    
    return date_ranges

def format_date_range_info(date_ranges):
    """
    Format date ranges for display.
    
    Args:
        date_ranges: List of tuples containing (start_date, end_date)
    
    Returns:
        Formatted string for display
    """
    if len(date_ranges) == 1:
        return "Analysis will run on the selected date range in one go."
    else:
        info = f"⚠️ Large date range detected! Analysis will be split into **{len(date_ranges)} monthly segments** to ensure optimal performance:\n\n"
        for idx, (start, end) in enumerate(date_ranges, 1):
            info += f"{idx}. {start.strftime('%d %b %Y')} to {end.strftime('%d %b %Y')}\n"
        return info

# ============================================================================
# TRADINGAGENTS FRAMEWORK SECTION
# ============================================================================

st.header("🤖 Trading Agents ")

st.markdown("""
### About TradingAgents
TradingAgents is a multi-agent trading models that mirrors the dynamics of real-world trading firms. 
By deploying specialized LLM-powered agents, the platform collaboratively evaluates market conditions and informs trading decisions.

**The Agent Team consists of:**
1. **Analyst Team**: Fundamentals, Sentiment, News, and Technical analysts
2. **Research Team**: Bull and Bear researchers with Research Manager
3. **Trading Team**: Trader agent that synthesizes insights
4. **Risk Management**: Aggressive, Conservative, and Neutral analysts
5. **Portfolio Management**: Final decision maker

*Note: This Agent Team is designed for research purposes. Trading performance may vary based on many factors.*
""")

st.markdown("---")

# Configuration Section
st.subheader("⚙️ Configuration")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🔑 API Keys Configuration")
    st.info("💡 Set your API keys as environment variables or enter them below.")
    
    # LLM Provider Selection
    llm_provider = st.selectbox(
        "Select LLM Provider",
        options=["Google", "OpenRouter", "Groq"],
        help="Choose your preferred LLM provider"
    )
    
    # API Key inputs based on provider
    if llm_provider == "Google":
        google_api_key = st.text_input(
            "Google API Key",
            type="password",
            value=os.getenv("GOOGLE_API_KEY", ""),
            help="Enter your Google AI API key"
        )
        if google_api_key:
            os.environ["GOOGLE_API_KEY"] = google_api_key
    
    elif llm_provider == "OpenRouter":
        openrouter_api_key = st.text_input(
            "OpenRouter API Key",
            type="password",
            value=os.getenv("OPENROUTER_API_KEY", ""),
            help="Enter your OpenRouter API key"
        )
        if openrouter_api_key:
            os.environ["OPENROUTER_API_KEY"] = openrouter_api_key
    
    elif llm_provider == "Groq":
        groq_api_key = st.text_input(
            "Groq API Key",
            type="password",
            value=os.getenv("GROQ_API_KEY", ""),
            help="Enter your Groq API key"
        )
        if groq_api_key:
            os.environ["GROQ_API_KEY"] = groq_api_key
    
    # Data Source Configuration
    st.markdown("---")
    st.markdown("#### 📊 Data Source Configuration")
    
    data_vendor = st.selectbox(
        "Select Data Vendor",
        options=["Yahoo Finance (yfinance)", "Alpha Vantage"],
        index=0,
        help="Choose your data source. Yahoo Finance is free and requires no API key. Alpha Vantage requires an API key but offers more detailed data."
    )
    
    # Show appropriate message based on selection
    if data_vendor == "Yahoo Finance (yfinance)":
        st.info("📊 Yahoo Finance selected - No API key required!")
        st.caption("✓ Unlimited requests | ✓ Free access | ✓ No rate limits")
        alpha_vantage_key = None
    else:
        st.info("🔑 Alpha Vantage selected - API key required")
        st.caption("⚡ Auto-fallback to Yahoo Finance if rate limit exceeded")
        alpha_vantage_key = st.text_input(
            "Alpha Vantage API Key",
            type="password",
            value=os.getenv("ALPHA_VANTAGE_API_KEY", ""),
            help="Get your free API key from https://www.alphavantage.co/support/#api-key"
        )
        if alpha_vantage_key:
            os.environ["ALPHA_VANTAGE_API_KEY"] = alpha_vantage_key
            st.success("✅ API key set (Free tier: 25 requests/day, 5/minute)")
        else:
            st.warning("⚠️ Alpha Vantage API key is required to fetch data")

with col2:
    st.markdown("#### 🎯 Trading Parameters")
    
    # Popular tickers with categories - format: "Name - SYMBOL"
    POPULAR_TICKERS = {
        "Major Indices": [
            ("S&P 500 ETF", "SPY"),
            ("Nasdaq 100 ETF", "QQQ"),
            ("Dow Jones ETF", "DIA"),
            ("Russell 2000 ETF", "IWM"),
            ("Total Stock Market ETF", "VTI")
        ],
        "Tech Stocks": [
            ("Apple", "AAPL"),
            ("Microsoft", "MSFT"),
            ("Alphabet (Google)", "GOOGL"),
            ("Amazon", "AMZN"),
            ("Meta (Facebook)", "META"),
            ("NVIDIA", "NVDA"),
            ("Tesla", "TSLA"),
            ("Netflix", "NFLX")
        ],
        "Blue Chip Stocks": [
            ("JPMorgan Chase", "JPM"),
            ("Bank of America", "BAC"),
            ("Walmart", "WMT"),
            ("Johnson & Johnson", "JNJ"),
            ("Visa", "V"),
            ("Mastercard", "MA"),
            ("Procter & Gamble", "PG"),
            ("Coca-Cola", "KO")
        ],
        "Cryptocurrencies": [
            ("Bitcoin", "BTC-USD"),
            ("Ethereum", "ETH-USD"),
            ("Binance Coin", "BNB-USD"),
            ("Cardano", "ADA-USD"),
            ("Solana", "SOL-USD"),
            ("Dogecoin", "DOGE-USD")
        ],
        "Forex Pairs": [
            ("Euro / US Dollar", "EURUSD=X"),
            ("British Pound / US Dollar", "GBPUSD=X"),
            ("US Dollar / Japanese Yen", "USDJPY=X"),
            ("US Dollar / Canadian Dollar", "USDCAD=X"),
            ("Australian Dollar / US Dollar", "AUDUSD=X"),
            ("US Dollar / Swiss Franc", "USDCHF=X"),
            ("New Zealand Dollar / US Dollar", "NZDUSD=X")
        ],
        "Commodities": [
            ("Gold Futures", "GC=F"),
            ("Silver Futures", "SI=F"),
            ("Crude Oil Futures", "CL=F"),
            ("Natural Gas Futures", "NG=F")
        ]
    }
    
    # Flatten the ticker list for selectbox with display names
    all_tickers_display = []
    ticker_map = {}  # Map display name to ticker symbol
    
    for category, tickers in POPULAR_TICKERS.items():
        for name, symbol in tickers:
            display_name = f"{name} - {symbol}"
            all_tickers_display.append(display_name)
            ticker_map[display_name] = symbol
    
    # Add custom option
    ticker_option = st.selectbox(
        "Select Stock/Crypto/Forex",
        options=["Custom"] + all_tickers_display,
        index=1,  # Default to first ticker (S&P 500 ETF - SPY)
        help="Select from popular tickers or choose 'Custom' to enter your own"
    )
    
    # If custom selected, show text input
    if ticker_option == "Custom":
        ticker = st.text_input(
            "Enter Custom Ticker",
            value="SPY",
            help="Enter stock ticker symbol (e.g., AAPL), crypto (BTC-USD), or forex pair (EURUSD=X)"
        ).upper()
    else:
        ticker = ticker_map[ticker_option]
    
    # Display ticker category
    ticker_category = None
    for category, tickers in POPULAR_TICKERS.items():
        for name, symbol in tickers:
            if ticker == symbol:
                ticker_category = category
                break
        if ticker_category:
            break
    if ticker_category:
        st.caption(f"📊 Category: {ticker_category}")
    
    # Date range selection
    st.markdown("**📅 Date Range Selection**")
    date_col1, date_col2 = st.columns(2)
    
    with date_col1:
        start_date = st.date_input(
            "From Date",
            value=datetime.now().date() - timedelta(days=30),
            max_value=datetime.now().date(),
            help="Start date for analysis (cannot be in the future)"
        )
    
    with date_col2:
        end_date = st.date_input(
            "To Date",
            value=datetime.now().date() - timedelta(days=1),
            max_value=datetime.now().date(),
            help="End date for analysis (cannot be in the future)"
        )
    
    # Validate date range
    if start_date > end_date:
        st.error("⚠️ Start date must be before or equal to end date!")
        date_ranges = []
    else:
        # Calculate date ranges (will chunk if needed)
        date_ranges = calculate_date_ranges(start_date, end_date)
        
        # Display info about chunking
        if len(date_ranges) > 1:
            st.info(format_date_range_info(date_ranges))
        else:
            days_diff = (end_date - start_date).days
            st.caption(f"📊 Analyzing {days_diff + 1} day(s) of data")
    
    # Analyst selection
    st.markdown("**Select Analyst Team:**")
    analyst_cols = st.columns(2)
    
    with analyst_cols[0]:
        market_analyst = st.checkbox("Market Analyst", value=True)
        social_analyst = st.checkbox("Social Media Analyst", value=True)
    
    with analyst_cols[1]:
        news_analyst = st.checkbox("News Analyst", value=True)
        fundamentals_analyst = st.checkbox("Fundamentals Analyst", value=True)
    
    # Research depth
    research_depth = st.select_slider(
        "Research Depth",
        options=[1, 2, 3, 4, 5],
        value=1,
        help="Number of debate rounds between agents (1=Shallow, 5=Deep)"
    )
    
    verbose_mode = st.checkbox(
        "Show Verbose Logs",
        value=False,
        help="Display detailed agent communication and data fetching logs"
    )

st.markdown("---")

# Model Selection Section
st.subheader("🧠 Model Selection")

# Define model options based on provider
MODEL_OPTIONS = {
    "Google": {
        "quick": [
            "gemini-flash-lite-latest",
            "gemini-2.0-flash-lite",
            "gemini-2.5-flash-lite",
            "gemini-flash-latest"
        ],
        "deep": [
            "gemini-3-pro-preview",
            "gemini-2.5-pro",
            "gemini-2.5-flash",
            "gemini-2.0-flash"
        ]
    },
    "OpenRouter": {
        "quick": [
            "meta-llama/llama-4-scout:free",
            "meta-llama/llama-3.3-8b-instruct:free",
            "google/gemini-2.0-flash-exp:free"
        ],
        "deep": [
            "meta-llama/llama-3.3-8b-instruct:free",
            "deepseek/deepseek-chat-v3-0324:free"
        ]
    },
    "Groq": {
        "quick": [
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile",
            "meta-llama/llama-4-maverick-17b-128e-instruct",
            "meta-llama/llama-4-scout-17b-16e-instruct"
        ],
        "deep": [
            "llama-3.3-70b-versatile",
            "meta-llama/llama-4-maverick-17b-128e-instruct",
            "meta-llama/llama-4-scout-17b-16e-instruct",
            "meta-llama/llama-guard-4-12b"
        ]
    }
}

model_col1, model_col2 = st.columns(2)

with model_col1:
    st.markdown("#### ⚡ Quick-Thinking Model")
    st.caption("Used for fast reasoning tasks and analysis")
    quick_model = st.selectbox(
        "Select Quick-Thinking Model",
        options=MODEL_OPTIONS[llm_provider]["quick"],
        help="Fast model for quick tasks and initial analysis"
    )

with model_col2:
    st.markdown("#### 🧠 Deep-Thinking Model")
    st.caption("Used for complex reasoning and decision-making")
    deep_model = st.selectbox(
        "Select Deep-Thinking Model",
        options=MODEL_OPTIONS[llm_provider]["deep"],
        help="Advanced model for deep analysis and strategic decisions"
    )

st.markdown("---")

# Run Analysis Section
st.subheader("🚀 Run Analysis")

# Prepare selected analysts
selected_analysts = []
analyst_mapping = {
    market_analyst: "market",
    social_analyst: "social",
    news_analyst: "news",
    fundamentals_analyst: "fundamentals"
}

for checkbox, analyst_type in analyst_mapping.items():
    if checkbox:
        selected_analysts.append(analyst_type)

# Validation
can_run = True
error_messages = []

if start_date > end_date:
    can_run = False
    error_messages.append("⚠️ Start date must be before or equal to end date")

if not date_ranges:
    can_run = False
    error_messages.append("⚠️ Invalid date range")

if not selected_analysts:
    can_run = False
    error_messages.append("⚠️ Please select at least one analyst")

if llm_provider == "Google" and not os.getenv("GOOGLE_API_KEY"):
    can_run = False
    error_messages.append("⚠️ Google API Key is required")

if llm_provider == "OpenRouter" and not os.getenv("OPENROUTER_API_KEY"):
    can_run = False
    error_messages.append("⚠️ OpenRouter API Key is required")

if llm_provider == "Groq" and not os.getenv("GROQ_API_KEY"):
    can_run = False
    error_messages.append("⚠️ Groq API Key is required")

if data_vendor == "Alpha Vantage" and not os.getenv("ALPHA_VANTAGE_API_KEY"):
    can_run = False
    error_messages.append("⚠️ Alpha Vantage API Key is required")

# Display errors if any
if error_messages:
    for msg in error_messages:
        st.error(msg)

# Run button
if st.button("🚀 Start TradingAgents Analysis", disabled=not can_run, type="primary"):
    try:
        # Import TradingAgents
        from tradingagents.graph.trading_graph import TradingAgentsGraph
        from tradingagents.default_config import DEFAULT_CONFIG
        
        # Create progress containers
        progress_container = st.container()
        results_container = st.container()
        
        # Create log container if verbose mode is enabled
        if verbose_mode:
            log_container = st.expander("📋 Detailed Logs", expanded=False)
            log_placeholder = log_container.empty()
            captured_logs = []
        
        with progress_container:
            if len(date_ranges) > 1:
                st.info(f"🔄 Analyzing {ticker} across {len(date_ranges)} time segments...")
            else:
                st.info(f"🔄 Initializing TradingAgents for {ticker} from {start_date} to {end_date}...")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Configure the framework
            config = DEFAULT_CONFIG.copy()
            config["llm_provider"] = llm_provider.lower()
            config["quick_think_llm"] = quick_model
            config["deep_think_llm"] = deep_model
            config["max_debate_rounds"] = research_depth
            config["max_risk_discuss_rounds"] = research_depth
            
            # Configure data vendor with fallback
            vendor = "alpha_vantage" if data_vendor == "Alpha Vantage" else "yfinance"
            
            # Set primary vendor with automatic fallback to yfinance if Alpha Vantage fails
            fallback_vendor = f"{vendor},yfinance" if vendor == "alpha_vantage" else vendor
            
            config["data_vendors"] = {
                "core_stock_apis": fallback_vendor,
                "technical_indicators": fallback_vendor,
                "fundamental_data": fallback_vendor,
                "news_data": fallback_vendor,
            }
            
            # Show info about fallback if using Alpha Vantage
            if vendor == "alpha_vantage":
                status_text.text("Using Alpha Vantage (will fallback to Yahoo Finance if needed)...")
            
            # Set backend URL based on provider
            if llm_provider == "Google":
                config["backend_url"] = "https://generativelanguage.googleapis.com/v1"
            elif llm_provider == "OpenRouter":
                config["backend_url"] = "https://openrouter.ai/api/v1"
            elif llm_provider == "Groq":
                config["backend_url"] = "https://api.groq.com/openai/v1"
            
            status_text.text("Initializing agents...")
            progress_bar.progress(5)
            
            # Capture stdout/stderr if not in verbose mode
            if not verbose_mode:
                # Suppress all console output
                stdout_capture = io.StringIO()
                stderr_capture = io.StringIO()
                stdout_context = redirect_stdout(stdout_capture)
                stderr_context = redirect_stderr(stderr_capture)
                stdout_context.__enter__()
                stderr_context.__enter__()
            
            try:
                # Initialize the graph
                graph = TradingAgentsGraph(selected_analysts, config=config, debug=verbose_mode)
            except Exception as e:
                if not verbose_mode:
                    stdout_context.__exit__(None, None, None)
                    stderr_context.__exit__(None, None, None)
                raise e
            
            # Helper function to extract URLs from text
            import re
            def extract_urls(text):
                if not text:
                    return []
                url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
                return re.findall(url_pattern, text)
            
            # Store all segment results
            all_segments_results = []
            segment_decisions = []
            all_sources = []
            
            # Process each date range segment
            total_segments = len(date_ranges)
            for segment_idx, (seg_start, seg_end) in enumerate(date_ranges, 1):
                status_text.text(f"Running analysis for segment {segment_idx}/{total_segments}: {seg_start.strftime('%d %b')} to {seg_end.strftime('%d %b')}...")
                base_progress = 10 + (segment_idx - 1) * (70 // total_segments)
                progress_bar.progress(base_progress)
                
                # Capture logs if in verbose mode
                if verbose_mode:
                    segment_stdout = io.StringIO()
                    segment_stderr = io.StringIO()
                    with redirect_stdout(segment_stdout), redirect_stderr(segment_stderr):
                        segment_state, segment_decision = graph.propagate(ticker, str(seg_end))
                    
                    # Capture and display logs
                    stdout_content = segment_stdout.getvalue()
                    stderr_content = segment_stderr.getvalue()
                    if stdout_content or stderr_content:
                        captured_logs.append(f"\n{'='*60}\nSegment {segment_idx}: {seg_start.strftime('%d %b')} to {seg_end.strftime('%d %b')}\n{'='*60}\n")
                        if stdout_content:
                            captured_logs.append(stdout_content)
                        if stderr_content:
                            captured_logs.append(f"\n--- Errors ---\n{stderr_content}")
                        log_placeholder.code(''.join(captured_logs), language='text')
                else:
                    # Run the analysis for this segment using the end date
                    segment_state, segment_decision = graph.propagate(ticker, str(seg_end))
                
                # Store segment results
                segment_result = {
                    "start_date": str(seg_start),
                    "end_date": str(seg_end),
                    "state": segment_state,
                    "decision": segment_decision
                }
                all_segments_results.append(segment_result)
                segment_decisions.append(segment_decision)
                
                # Extract sources from this segment
                segment_sources = []
                for report_key in ["market_report", "sentiment_report", "news_report", "fundamentals_report"]:
                    if segment_state.get(report_key):
                        urls = extract_urls(segment_state[report_key])
                        segment_sources.extend(urls)
                
                if segment_state.get("investment_debate_state"):
                    debate_state = segment_state["investment_debate_state"]
                    for key in ["bull_history", "bear_history", "judge_decision"]:
                        if debate_state.get(key):
                            urls = extract_urls(debate_state[key])
                            segment_sources.extend(urls)
                
                all_sources.extend(segment_sources)
            
            # Use the last segment as the primary final state
            final_state = all_segments_results[-1]["state"]
            decision = all_segments_results[-1]["decision"]
            
            status_text.text("Consolidating results...")
            progress_bar.progress(85)
            
            # Remove duplicate sources while preserving order
            sources = list(dict.fromkeys(all_sources))
            
            # Store analysis results in session state
            st.session_state.trading_analysis = {
                "ticker": ticker,
                "start_date": str(start_date),
                "end_date": str(end_date),
                "date_ranges": [(str(s), str(e)) for s, e in date_ranges],
                "all_segments_results": all_segments_results,
                "segment_decisions": segment_decisions,
                "final_state": final_state,
                "decision": decision,
                "sources": sources,
                "timestamp": datetime.now().isoformat()
            }
            
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
        
        # Display results
        with results_container:
            st.success(f"🎉 Analysis completed successfully for {start_date.strftime('%d %b %Y')} to {end_date.strftime('%d %b %Y')}!")
            
            # Show segment overview if multiple segments
            if len(date_ranges) > 1:
                with st.expander(f"📅 View All {len(date_ranges)} Time Segments Analysis", expanded=False):
                    for idx, segment_result in enumerate(all_segments_results, 1):
                        st.markdown(f"### Segment {idx}: {segment_result['start_date']} to {segment_result['end_date']}")
                        st.info(f"**Decision:** {segment_result['decision']}")
                        if idx < len(all_segments_results):
                            st.markdown("---")
            
            # Create tabs for different reports
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📊 Analyst Reports", 
                "🔍 Research Team", 
                "💼 Trading Plan", 
                "⚠️ Risk Assessment", 
                "✅ Final Decision"
            ])
            
            with tab1:
                st.markdown("### Analyst Team Reports")
                
                if final_state.get("market_report"):
                    with st.expander("📈 Market Analyst Report", expanded=True):
                        st.markdown(final_state["market_report"])
                
                if final_state.get("sentiment_report"):
                    with st.expander("💬 Social Media Analyst Report", expanded=True):
                        st.markdown(final_state["sentiment_report"])
                
                if final_state.get("news_report"):
                    with st.expander("📰 News Analyst Report", expanded=True):
                        st.markdown(final_state["news_report"])
                
                if final_state.get("fundamentals_report"):
                    with st.expander("📊 Fundamentals Analyst Report", expanded=True):
                        st.markdown(final_state["fundamentals_report"])
            
            with tab2:
                st.markdown("### Research Team Analysis")
                
                if final_state.get("investment_debate_state"):
                    debate_state = final_state["investment_debate_state"]
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if debate_state.get("bull_history"):
                            st.markdown("#### 🐂 Bull Researcher")
                            st.info(debate_state["bull_history"])
                    
                    with col2:
                        if debate_state.get("bear_history"):
                            st.markdown("#### 🐻 Bear Researcher")
                            st.warning(debate_state["bear_history"])
                    
                    if debate_state.get("judge_decision"):
                        st.markdown("#### 👨‍⚖️ Research Manager Decision")
                        st.success(debate_state["judge_decision"])
            
            with tab3:
                st.markdown("### Trading Team Plan")
                
                if final_state.get("trader_investment_plan"):
                    st.markdown(final_state["trader_investment_plan"])
                else:
                    st.info("No trading plan generated")
            
            with tab4:
                st.markdown("### Risk Management Assessment")
                
                if final_state.get("risk_debate_state"):
                    risk_state = final_state["risk_debate_state"]
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if risk_state.get("risky_history"):
                            st.markdown("#### 🔴 Aggressive Analyst")
                            st.error(risk_state["risky_history"])
                    
                    with col2:
                        if risk_state.get("neutral_history"):
                            st.markdown("#### 🟡 Neutral Analyst")
                            st.warning(risk_state["neutral_history"])
                    
                    with col3:
                        if risk_state.get("safe_history"):
                            st.markdown("#### 🟢 Conservative Analyst")
                            st.success(risk_state["safe_history"])
            
            with tab5:
                st.markdown("### 🏆 Portfolio Manager Final Decision")
                st.caption(f"Based on analysis from {start_date.strftime('%d %b %Y')} to {end_date.strftime('%d %b %Y')}")
                
                if final_state.get("risk_debate_state", {}).get("judge_decision"):
                    st.markdown(final_state["risk_debate_state"]["judge_decision"])
                
                st.markdown("---")
                st.markdown("#### 📋 Trading Signal")
                
                # Display the processed decision
                if decision:
                    # Create a proper JSON structure for the trading signal
                    signal_data = {
                        "ticker": ticker,
                        "start_date": str(start_date),
                        "end_date": str(end_date),
                        "segments_analyzed": len(date_ranges),
                        "decision": decision.strip() if isinstance(decision, str) else str(decision),
                        "timestamp": datetime.now().isoformat()
                    }
                    st.json(signal_data)
                    
                    # Display a visual indicator
                    if "BUY" in decision.upper():
                        st.success(f"🟢 **SIGNAL: BUY {ticker}**")
                    elif "SELL" in decision.upper():
                        st.error(f"🔴 **SIGNAL: SELL {ticker}**")
                    elif "HOLD" in decision.upper():
                        st.warning(f"🟡 **SIGNAL: HOLD {ticker}**")
                    else:
                        st.info(f"📊 **SIGNAL: {decision}**")
                else:
                    st.info("No final decision available")
                
                # Display sources section
                if sources:
                    st.markdown("---")
                    st.markdown("### 📚 Sources & References")
                    st.markdown("""
                    The analysis above is based on data from the following sources. 
                    Click on any link below to verify the information:
                    """)
                    
                    # Create columns for better layout
                    source_cols = st.columns(2)
                    
                    for idx, source_url in enumerate(sources):
                        col_idx = idx % 2
                        with source_cols[col_idx]:
                            # Try to extract domain name for display
                            try:
                                from urllib.parse import urlparse
                                domain = urlparse(source_url).netloc
                                display_text = f"🔗 {domain}"
                            except:
                                display_text = "🔗 Source Link"
                            
                            st.markdown(f"[{display_text}]({source_url})")
                    
                    st.info(f"💡 Total {len(sources)} source(s) referenced in this analysis")
                else:
                    st.markdown("---")
                    st.markdown("### 📚 Sources & References")
                    
                    st.info("No external sources were explicitly referenced in this analysis. The data comes from Yahoo Finance and technical indicators.")
            
            # Clean up stdout/stderr capture if it was used
            if not verbose_mode:
                stdout_context.__exit__(None, None, None)
                stderr_context.__exit__(None, None, None)
    
    except Exception as e:
        # Clean up stdout/stderr capture in case of error
        if not verbose_mode:
            try:
                stdout_context.__exit__(None, None, None)
                stderr_context.__exit__(None, None, None)
            except:
                pass
        st.error(f"❌ Error during analysis: {str(e)}")
        st.exception(e)

st.markdown("---")
st.info("Use the **left sidebar** to select a module.")

