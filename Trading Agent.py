import streamlit as st
import os
import sys
from datetime import datetime, timedelta

# Add TradingAgents to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'TradingAgents'))

# Set page config
st.set_page_config(
    # page_title="📊 AI Investment Dashboard",
    # page_icon="📈",
    layout="wide"
)

# ============================================================================
# TRADINGAGENTS FRAMEWORK SECTION
# ============================================================================

st.header("🤖 TradingAgents Framework")

st.markdown("""
### About TradingAgents
TradingAgents is a multi-agent trading framework that mirrors the dynamics of real-world trading firms. 
By deploying specialized LLM-powered agents, the platform collaboratively evaluates market conditions and informs trading decisions.

**The framework consists of:**
1. **Analyst Team**: Fundamentals, Sentiment, News, and Technical analysts
2. **Research Team**: Bull and Bear researchers with Research Manager
3. **Trading Team**: Trader agent that synthesizes insights
4. **Risk Management**: Aggressive, Conservative, and Neutral analysts
5. **Portfolio Management**: Final decision maker

*Note: This framework is designed for research purposes. Trading performance may vary based on many factors.*
""")

with st.expander("📚 View Complete Framework Documentation", expanded=False):
    readme_path = os.path.join(os.path.dirname(__file__), 'TradingAgents', 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
        st.markdown(readme_content)
    else:
        st.warning("README.md not found in TradingAgents directory")

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
    
    # Alpha Vantage API (required for data)
    alpha_vantage_key = st.text_input(
        "Alpha Vantage API Key",
        type="password",
        value=os.getenv("ALPHA_VANTAGE_API_KEY", ""),
        help="Required for fundamental and news data. Get free API: https://www.alphavantage.co/support/#api-key"
    )
    if alpha_vantage_key:
        os.environ["ALPHA_VANTAGE_API_KEY"] = alpha_vantage_key

with col2:
    st.markdown("#### 🎯 Trading Parameters")
    
    # Ticker input
    ticker = st.text_input(
        "Stock Ticker",
        value="SPY",
        help="Enter stock ticker symbol (e.g., AAPL, TSLA, SPY)"
    ).upper()
    
    # Date selection
    analysis_date = st.date_input(
        "Analysis Date",
        value=datetime.now().date() - timedelta(days=1),
        max_value=datetime.now().date(),
        help="Select the date for analysis (cannot be in the future)"
    )
    
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

st.markdown("---")

# Model Selection Section
st.subheader("🧠 Model Selection")

# Define model options based on provider
MODEL_OPTIONS = {
    "Google": {
        "quick": [
            "gemini-2.0-flash-lite",
            "gemini-2.0-flash",
            "gemini-2.5-flash-preview-05-20"
        ],
        "deep": [
            "gemini-2.0-flash",
            "gemini-2.5-flash-preview-05-20",
            "gemini-2.5-pro-preview-06-05"
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

if not os.getenv("ALPHA_VANTAGE_API_KEY"):
    can_run = False
    error_messages.append("⚠️ Alpha Vantage API Key is required for data access")

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
        
        with progress_container:
            st.info(f"🔄 Initializing TradingAgents for {ticker} on {analysis_date}...")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Configure the framework
            config = DEFAULT_CONFIG.copy()
            config["llm_provider"] = llm_provider.lower()
            config["quick_think_llm"] = quick_model
            config["deep_think_llm"] = deep_model
            config["max_debate_rounds"] = research_depth
            config["max_risk_discuss_rounds"] = research_depth
            
            # Set backend URL based on provider
            if llm_provider == "Google":
                config["backend_url"] = "https://generativelanguage.googleapis.com/v1"
            elif llm_provider == "OpenRouter":
                config["backend_url"] = "https://openrouter.ai/api/v1"
            elif llm_provider == "Groq":
                config["backend_url"] = "https://api.groq.com/openai/v1"
            
            status_text.text("Initializing agents...")
            progress_bar.progress(10)
            
            # Initialize the graph
            graph = TradingAgentsGraph(selected_analysts, config=config, debug=True)
            
            status_text.text("Running analysis workflow...")
            progress_bar.progress(30)
            
            # Run the analysis
            final_state, decision = graph.propagate(ticker, str(analysis_date))
            
            # Store analysis results in session state
            st.session_state.trading_analysis = {
                "ticker": ticker,
                "analysis_date": str(analysis_date),
                "final_state": final_state,
                "decision": decision,
                "timestamp": datetime.now().isoformat()
            }
            
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
        
        # Display results
        with results_container:
            st.success("🎉 Analysis completed successfully!")
            
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
                
                if final_state.get("risk_debate_state", {}).get("judge_decision"):
                    st.markdown(final_state["risk_debate_state"]["judge_decision"])
                
                st.markdown("---")
                st.markdown("#### 📋 Trading Signal")
                
                # Display the processed decision
                if decision:
                    # Create a proper JSON structure for the trading signal
                    signal_data = {
                        "ticker": ticker,
                        "analysis_date": str(analysis_date),
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
    
    except Exception as e:
        st.error(f"❌ Error during analysis: {str(e)}")
        st.exception(e)

st.markdown("---")
st.info("Use the **left sidebar** to select a module.")

