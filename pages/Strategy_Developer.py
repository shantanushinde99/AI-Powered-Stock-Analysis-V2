import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import json
import os
import sys
from pathlib import Path
from groq import Groq
import google.generativeai as genai
from PIL import Image
import io
import plotly.graph_objects as go
import plotly.express as px
from streamlit.components.v1 import html

# Add parent path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.styles import get_tradeguide_styles, get_sidebar_html, get_page_header

# GCP Video URLs
VIDEO_1_URL = "https://storage.googleapis.com/stock-project-videos/video1_hls/video1_hls.m3u8"
VIDEO_2_URL = "https://storage.googleapis.com/stock-project-videos/video2_hls/video2_hls.m3u8"


def hls_player(video_url: str, video_id: str, height: int = 420):
    """HLS video player component for streaming videos from GCP"""
    html(
        f"""
        <video id="{video_id}" controls preload="metadata"
               style="width:100%; height:{height}px; border-radius:10px;"></video>

        <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
        <script>
            const video = document.getElementById("{video_id}");
            const source = "{video_url}";

            if (Hls.isSupported()) {{
                const hls = new Hls({{
                    enableWorker: true,
                    lowLatencyMode: true,
                    backBufferLength: 90
                }});
                hls.loadSource(source);
                hls.attachMedia(video);
            }} else if (video.canPlayType('application/vnd.apple.mpegurl')) {{
                video.src = source;
            }}
        </script>
        """,
        height=height + 80
    )

# Page configuration
st.set_page_config(
    page_title="Strategy Developer - TradeGuide AI",
    page_icon="🎯",
    layout="wide"
)

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
st.markdown(get_page_header("🎯 Strategy Developer", "Build and test your trading strategies step-by-step"), unsafe_allow_html=True)

# Initialize session state variables
if 'strategy_data' not in st.session_state:
    st.session_state.strategy_data = {
        'instrument': None,
        'entry_rules': '',
        'exit_rules': '',
        'stop_loss': '',
        'take_profit': '',
        'strategy_description': '',
        'time_window': None,
        'trades': [],
        'chart_analysis': None
    }

if 'gemini_api_key' not in st.session_state:
    st.session_state.gemini_api_key = ''

if 'groq_api_key' not in st.session_state:
    st.session_state.groq_api_key = ''

if 'rephrased_content' not in st.session_state:
    st.session_state.rephrased_content = None

if 'compliance_analysis' not in st.session_state:
    st.session_state.compliance_analysis = None

if 'knows_strategy_building' not in st.session_state:
    st.session_state.knows_strategy_building = None

if 'show_strategy_setup' not in st.session_state:
    st.session_state.show_strategy_setup = False

# File path for persistent storage
DATA_DIR = Path("strategy_data")
DATA_DIR.mkdir(exist_ok=True)

def save_strategy_data():
    """Save strategy data to JSON file"""
    if st.session_state.strategy_data['instrument']:
        filename = DATA_DIR / f"{st.session_state.strategy_data['instrument'].replace('/', '_')}_strategy.json"
        with open(filename, 'w') as f:
            # Convert datetime objects to strings for JSON serialization
            data_to_save = st.session_state.strategy_data.copy()
            for trade in data_to_save['trades']:
                if isinstance(trade.get('date_time'), datetime):
                    trade['date_time'] = trade['date_time'].isoformat()
            json.dump(data_to_save, f, indent=4)
        return True
    return False

def load_strategy_data(instrument):
    """Load strategy data from JSON file"""
    filename = DATA_DIR / f"{instrument.replace('/', '_')}_strategy.json"
    if filename.exists():
        with open(filename, 'r') as f:
            data = json.load(f)
            # Convert ISO strings back to datetime objects
            for trade in data['trades']:
                if isinstance(trade.get('date_time'), str):
                    try:
                        trade['date_time'] = datetime.fromisoformat(trade['date_time'])
                    except:
                        trade['date_time'] = datetime.now()
            return data
    return None

def rephrase_strategy_with_groq(instrument, strategy_description, entry_rules, exit_rules, stop_loss, take_profit, api_key):
    """Rephrase user's strategy input using Groq - only corrects grammar without adding or editing content"""
    try:
        client = Groq(api_key=api_key)
        
        prompt = f"""You are a professional text editor. Your ONLY job is to rephrase the following trading strategy information to correct any grammatical errors, typos, or sentence structure issues.

CRITICAL RULES:
1. DO NOT add any new information or sentences
2. DO NOT remove any information provided by the user
3. DO NOT change the meaning of any sentences
4. ONLY fix grammar, spelling, punctuation, and sentence structure
5. Keep the same tone and style as the original
6. If a section is empty or missing, keep it empty - DO NOT add placeholder text
7. Preserve all technical terms and trading terminology exactly as written
8. Format the output with proper markdown styling

FORMATTING RULES:
- Make all section titles BOLD using **Title** format
- If content has points/list items, format them as proper bullet points using - or • symbols
- Maintain proper spacing between sections
- Keep the structure clean and readable

---USER'S INPUT---

Instrument: {instrument if instrument else '[Not provided]'}

Strategy Description:
{strategy_description if strategy_description else '[Not provided]'}

Entry Rules:
{entry_rules if entry_rules else '[Not provided]'}

Exit Rules:
{exit_rules if exit_rules else '[Not provided]'}

Stop-Loss Rules:
{stop_loss if stop_loss else '[Not provided]'}

Take-Profit Rules:
{take_profit if take_profit else '[Not provided]'}

---END OF USER'S INPUT---

Please rephrase ONLY the sections that have content (ignore '[Not provided]' sections). Return the corrected text with proper markdown formatting:

**Instrument:** [corrected version or skip if not provided]

**Strategy Description:**
[corrected version with bullet points if applicable, or skip if not provided]

**Entry Rules:**
[corrected version with bullet points if applicable, or skip if not provided]

**Exit Rules:**
[corrected version with bullet points if applicable, or skip if not provided]

**Stop-Loss Rules:**
[corrected version with bullet points if applicable, or skip if not provided]

**Take-Profit Rules:**
[corrected version with bullet points if applicable, or skip if not provided]

IMPORTANT: If the user's content has multiple points or list items (e.g., separated by commas, semicolons, numbers, or line breaks), format them as clean bullet points using - or •. Otherwise, keep as paragraph format.
"""
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="openai/gpt-oss-120b",
            temperature=0.3,
        )
        
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error rephrasing strategy: {str(e)}"

def analyze_chart_with_gemini(image, api_key):
    """Analyze uploaded chart using Gemini models"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = """
        You are an expert trading analyst with deep knowledge of technical analysis, chart patterns, and trading psychology.
        Analyze this trading chart comprehensively and provide a detailed, actionable report.
        
        ## ANALYSIS FRAMEWORK:
        
        ### 1. CHART IDENTIFICATION & CONTEXT
        - Identify the asset/instrument if visible
        - Determine the timeframe (1m, 5m, 15m, 1H, 4H, Daily, etc.)
        - Assess overall market structure (trending, ranging, choppy, volatile)
        - Identify the current market phase (accumulation, markup, distribution, markdown)
        
        ### 2. TECHNICAL INDICATORS ANALYSIS
        **If indicators are present:**
        - List ALL visible indicators (EMAs, SMAs, RSI, MACD, Bollinger Bands, Volume, etc.)
        - Analyze each indicator's signal (bullish, bearish, neutral)
        - Check for indicator confluence or divergence
        - Note any overbought/oversold conditions
        
        **If NO indicators are visible:**
        - Recommend 3-5 essential indicators for this chart/timeframe
        - Explain why each indicator would be valuable
        - Suggest optimal settings for each indicator
        
        ### 3. PRICE ACTION ANALYSIS
        - Identify key support and resistance levels
        - Detect chart patterns (triangles, flags, head & shoulders, double tops/bottoms, etc.)
        - Analyze candlestick patterns (engulfing, doji, hammers, shooting stars, etc.)
        - Identify trend lines and channels
        - Note any breakouts, fakeouts, or reversals
        
        ### 4. TRADER'S EXECUTION REVIEW
        **If trade entries/exits are marked:**
        - ✅ **Good Decisions:**
          * Well-timed entries with proper confirmation
          * Strategic exit points (profit-taking or stop-loss)
          * Evidence of following a plan
          * Good risk-reward setup
          * Proper position sizing indicators
        
        - ❌ **Mistakes & Improvement Areas:**
          * Premature or late entries
          * Chasing price or FOMO trades
          * Ignored warning signals
          * Poor stop-loss placement
          * Missing confluence factors
          * Overtrading or revenge trading signs
        
        **If NO trades are marked:**
        - Identify the BEST entry point(s) visible on the chart
        - E xplain the reasoning behind each entry signal
        - Suggest optimal stop-loss placement
        - Calculate potential take-profit targets (TP1, TP2, TP3)
        - Provide risk-reward ratio for suggested trades
        
        ### 5. STRATEGY RECOMMENDATIONS
        **Based on chart analysis, suggest:**
        
        **Entry Strategy:**
        - Specific entry conditions (e.g., "Enter long when price breaks above 50 EMA with volume confirmation")
        - Multiple entry techniques (aggressive vs conservative)
        - Confirmation signals to wait for
        
        **Exit Strategy:**
        - Take-profit levels (fixed targets or trailing stops)
        - Stop-loss placement rules
        - Partial profit-taking strategy
        - When to break even
        
        **Risk Management:**
        - Recommended position size (% of capital)
        - Maximum risk per trade
        - Risk-reward ratio targets
        
        ### 6. MARKET SCENARIO ASSESSMENT
        **Current Market State:**
        - Is it a good time to trade? (Yes/No/Wait)
        - What is the probability of success right now?
        - What are the key risks?
        - What should the trader watch for next?
        
        **Bullish Scenario:** If price does X, expect Y
        **Bearish Scenario:** If price does A, expect B
        **Neutral/Wait Scenario:** If conditions unclear, wait for Z
        
        ### 7. OVERALL RATING & RECOMMENDATIONS
        - **Execution Score:** Rate the trading execution from 1-10 (if trades visible)
        - **Chart Quality Score:** Rate the chart setup quality 1-10
        - **Recommended Action:** BUY / SELL / WAIT / AVOID
        
        **Key Takeaways (3-5 bullet points):**
        - Most important insights
        - Critical mistakes to avoid
        - Best practices to follow
        
        **Educational Tips:**
        - What this chart teaches us
        - Common pitfalls in similar setups
        - Advanced concepts to study further
        
        ---
        
        ## OUTPUT GUIDELINES:
        - Be specific with price levels, percentages, and numerical values
        - Use clear formatting with headers, bullets, and emojis
        - Provide actionable advice, not just descriptions
        - Be constructive and educational, not judgmental
        - If information is missing, suggest what's needed
        - Use professional trading terminology
        - Include both beginner-friendly and advanced insights
        
        ## IMPORTANT:
        - If the chart is empty or has minimal data, focus heavily on strategy recommendations
        - If trades are marked, prioritize execution review
        - Always provide value regardless of chart quality
        - Be honest about uncertainty or unclear signals
        
        Begin your analysis now:
        """
        
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"Error analyzing chart: {str(e)}"

def analyze_strategy_compliance_with_gemini(strategy_data, trades, api_key):
    """Analyze if trades follow the defined strategy using Gemini 2.5 Flash - Returns structured JSON data"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Smart sampling strategy based on total trades
        total_trades = len(trades)
        
        if total_trades <= 500:
            # Analyze all trades for comprehensive check
            trades_to_analyze = trades
            sampling_info = f"all {total_trades} trades"
        else:
            # Stratified sampling for large datasets (500+ trades)
            # Sample 150-200 trades evenly distributed across entire period
            target_sample_size = min(200, max(150, total_trades // 10))
            step = total_trades // target_sample_size
            trades_to_analyze = [trades[i] for i in range(0, total_trades, step)][:target_sample_size]
            sampling_info = f"{len(trades_to_analyze)} trades (stratified sample from {total_trades} total trades)"
        
        # Prepare trades summary
        trades_summary = []
        for idx, trade in enumerate(trades_to_analyze, 1):
            trade_info = f"""
Trade #{idx}:
- Date & Time: {trade.get('date_time', 'N/A')}
- Instrument: {trade.get('instrument', 'N/A')}
- Entry Price: {trade.get('entry_price', 'N/A')}
- Exit Price: {trade.get('exit_price', 'N/A')}
- Stop-Loss: {trade.get('stop_loss', 'N/A')}
- Take-Profit: {trade.get('take_profit', 'N/A')}
- Risk:Reward Ratio: {trade.get('rr_ratio', 'N/A')}
- Result: {trade.get('result', 'N/A')}
- Notes: {trade.get('notes', 'N/A')}
"""
            trades_summary.append(trade_info)
        
        trades_text = "\n".join(trades_summary)
        
        prompt = f"""You are an expert trading coach analyzing if a trader is following their defined trading strategy.

**DEFINED STRATEGY:**
- Instrument: {strategy_data.get('instrument', 'Not specified')}
- Time Window: {strategy_data.get('time_window', 'Not specified')}
- Strategy Description: {strategy_data.get('strategy_description', 'Not specified')}
- Entry Rules: {strategy_data.get('entry_rules', 'Not specified')}
- Exit Rules: {strategy_data.get('exit_rules', 'Not specified')}
- Stop-Loss Rules: {strategy_data.get('stop_loss', 'Not specified')}
- Take-Profit Rules: {strategy_data.get('take_profit', 'Not specified')}

**TRADES ANALYZED ({sampling_info}):**
{trades_text}

**RETURN FORMAT - STRICT JSON:**
Return your analysis in the following JSON format ONLY (no markdown, no code blocks, just pure JSON):

{{
  "compliance_score": 85,
  "overall_rating": "Good",
  "summary": "Brief 1-2 sentence summary of overall compliance",
  "metrics": {{
    "instrument_compliance": {{"score": 100, "status": "pass", "message": "All trades on correct instrument"}},
    "time_window_compliance": {{"score": 80, "status": "warning", "message": "2 trades outside time window"}},
    "risk_management": {{"score": 70, "status": "warning", "message": "Risk management could be improved"}},
    "entry_rules": {{"score": 90, "status": "pass", "message": "Following entry rules well"}},
    "exit_rules": {{"score": 75, "status": "warning", "message": "Premature exits detected"}},
    "stop_loss_usage": {{"score": 100, "status": "pass", "message": "Stop-loss used consistently"}},
    "take_profit_usage": {{"score": 60, "status": "fail", "message": "TP missing on 4 trades"}}
  }},
  "violations": [
    {{"severity": "critical", "title": "Wrong Instrument", "description": "Trade #3 was on EUR/USD instead of specified instrument", "trade_numbers": [3]}},
    {{"severity": "warning", "title": "Time Window", "description": "2 trades taken outside specified session", "trade_numbers": [5, 7]}},
    {{"severity": "suggestion", "title": "Risk Size", "description": "Consider reducing position size on some trades", "trade_numbers": [2, 6, 9]}}
  ],
  
**CRITICAL: The 'trade_numbers' array MUST contain the actual trade numbers (e.g., [1, 3, 5]) for every violation. NEVER leave this empty. If a violation applies to all trades, list all trade numbers.**
  "strengths": [
    "Consistent stop-loss placement",
    "Good R:R ratios maintained",
    "Following entry signals"
  ],
  "action_items": [
    "Stick to specified trading session only",
    "Set take-profit levels before entry",
    "Reduce position size to max 2% risk"
  ],
  "trade_analysis": [
    {{"trade_num": 1, "compliant": true, "issues": []}},
    {{"trade_num": 2, "compliant": false, "issues": ["High risk"]}},
    {{"trade_num": 3, "compliant": false, "issues": ["Wrong instrument", "Outside time window"]}}
  ]
}}

**SCORING RULES:**
- 90-100: pass (status: "pass")
- 70-89: warning (status: "warning")
- 0-69: fail (status: "fail")
- Overall compliance score is weighted average
- Severity levels: "critical", "warning", "suggestion"

Analyze the trades and return ONLY the JSON object, nothing else.
"""
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean response (remove markdown code blocks if present)
        if response_text.startswith('```'):
            response_text = response_text.split('```')[1]
            if response_text.startswith('json'):
                response_text = response_text[4:]
            response_text = response_text.strip()
        
        # Parse JSON
        analysis_data = json.loads(response_text)
        return analysis_data
        
    except Exception as e:
        # Return error in same format
        return {
            "compliance_score": 0,
            "overall_rating": "Error",
            "summary": f"Error analyzing compliance: {str(e)}",
            "metrics": {},
            "violations": [],
            "strengths": [],
            "action_items": [],
            "trade_analysis": []
        }

def display_compliance_dashboard(analysis_data):
    """Display beautiful compliance dashboard with cards and visualizations"""
    
    if not analysis_data or analysis_data.get('overall_rating') == 'Error':
        st.error(f"⚠️ {analysis_data.get('summary', 'Analysis failed')}")
        return
    
    # HEADER SECTION
    st.markdown("### 🎯 Strategy Compliance Dashboard")
    st.markdown(f"_{analysis_data.get('summary', '')}_")
    st.markdown("---")
    
    # TOP METRICS ROW - Compliance Score with Gauge
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        score = analysis_data.get('compliance_score', 0)
        rating = analysis_data.get('overall_rating', 'Unknown')
        
        # Create gauge chart
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Compliance Score", 'font': {'size': 20}},
            delta={'reference': 80, 'increasing': {'color': "green"}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 70], 'color': '#ffebee'},
                    {'range': [70, 90], 'color': '#fff9c4'},
                    {'range': [90, 100], 'color': '#e8f5e9'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig_gauge.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col2:
        st.markdown("<div style='text-align: center; padding: 20px;'>", unsafe_allow_html=True)
        if score >= 90:
            st.markdown("# 🟢")
            st.markdown("**Excellent**")
        elif score >= 70:
            st.markdown("# 🟡")
            st.markdown("**Good**")
        else:
            st.markdown("# 🔴")
            st.markdown("**Needs Work**")
        st.markdown(f"### {score}/100")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        violations = analysis_data.get('violations', [])
        critical = len([v for v in violations if v.get('severity') == 'critical'])
        warnings = len([v for v in violations if v.get('severity') == 'warning'])
        
        st.metric("🚨 Critical", critical)
        st.metric("⚠️ Warnings", warnings)
    
    with col4:
        strengths_count = len(analysis_data.get('strengths', []))
        actions_count = len(analysis_data.get('action_items', []))
        
        st.metric("✅ Strengths", strengths_count)
        st.metric("🎯 Actions", actions_count)
    
    st.markdown("---")
    
    # COMPLIANCE METRICS CARDS
    st.markdown("### 📊 Compliance Breakdown")
    
    metrics = analysis_data.get('metrics', {})
    if metrics:
        # Create 3 columns for metric cards
        metric_items = list(metrics.items())
        rows = [metric_items[i:i+3] for i in range(0, len(metric_items), 3)]
        
        for row in rows:
            cols = st.columns(len(row))
            for idx, (metric_name, metric_data) in enumerate(row):
                with cols[idx]:
                    score_val = metric_data.get('score', 0)
                    status = metric_data.get('status', 'unknown')
                    message = metric_data.get('message', '')
                    
                    # Status emoji and color
                    if status == 'pass':
                        emoji = "✅"
                        color = "#d4edda"
                        border_color = "#28a745"
                    elif status == 'warning':
                        emoji = "⚠️"
                        color = "#fff3cd"
                        border_color = "#ffc107"
                    else:
                        emoji = "❌"
                        color = "#f8d7da"
                        border_color = "#dc3545"
                    
                    # Display name formatting
                    display_name = metric_name.replace('_', ' ').title()
                    
                    # Card HTML
                    st.markdown(f"""
                    <div style='
                        padding: 15px;
                        border-radius: 10px;
                        background-color: {color};
                        border-left: 5px solid {border_color};
                        margin-bottom: 10px;
                    '>
                        <div style='font-size: 24px;'>{emoji}</div>
                        <div style='font-weight: bold; font-size: 16px; margin-top: 5px;'>{display_name}</div>
                        <div style='font-size: 28px; font-weight: bold; color: {border_color}; margin: 10px 0;'>{score_val}%</div>
                        <div style='font-size: 13px; color: #666;'>{message}</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # VIOLATIONS SECTION
    violations = analysis_data.get('violations', [])
    if violations:
        st.markdown("### 🚨 Issues & Violations")
        
        # Group by severity
        critical_violations = [v for v in violations if v.get('severity') == 'critical']
        warning_violations = [v for v in violations if v.get('severity') == 'warning']
        suggestion_violations = [v for v in violations if v.get('severity') == 'suggestion']
        
        # Critical Issues
        if critical_violations:
            st.markdown("#### 🚨 Critical Issues")
            for v in critical_violations:
                trade_nums = ", ".join([f"#{n}" for n in v.get('trade_numbers', [])])
                st.error(f"""
**{v.get('title', 'Issue')}**  
{v.get('description', '')}  
_Trades: {trade_nums}_
                """)
        
        # Warnings
        if warning_violations:
            st.markdown("#### ⚠️ Warnings")
            for v in warning_violations:
                trade_nums = ", ".join([f"#{n}" for n in v.get('trade_numbers', [])])
                st.warning(f"""
**{v.get('title', 'Warning')}**  
{v.get('description', '')}  
_Trades: {trade_nums}_
                """)
        
        # Suggestions
        if suggestion_violations:
            st.markdown("#### 💡 Suggestions")
            for v in suggestion_violations:
                trade_nums = ", ".join([f"#{n}" for n in v.get('trade_numbers', [])])
                st.info(f"""
**{v.get('title', 'Suggestion')}**  
{v.get('description', '')}  
_Trades: {trade_nums}_
                """)
    
    st.markdown("---")
    
    # TWO COLUMN SECTION - Strengths & Actions
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ What You're Doing Well")
        strengths = analysis_data.get('strengths', [])
        if strengths:
            for strength in strengths:
                st.success(f"✓ {strength}")
        else:
            st.info("Focus on building strengths!")
    
    with col2:
        st.markdown("### 🎯 Action Items")
        actions = analysis_data.get('action_items', [])
        if actions:
            for idx, action in enumerate(actions, 1):
                st.warning(f"{idx}. {action}")
        else:
            st.success("Keep up the great work!")
    
    st.markdown("---")
    
    # TRADE-BY-TRADE BREAKDOWN
    trade_analysis = analysis_data.get('trade_analysis', [])
    if trade_analysis:
        with st.expander("📋 Trade-by-Trade Breakdown", expanded=False):
            for trade in trade_analysis:
                trade_num = trade.get('trade_num', 0)
                compliant = trade.get('compliant', True)
                issues = trade.get('issues', [])
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    if compliant:
                        st.markdown(f"### ✅ #{trade_num}")
                    else:
                        st.markdown(f"### ❌ #{trade_num}")
                
                with col2:
                    if compliant:
                        st.success(f"Trade #{trade_num}: Following strategy ✓")
                    else:
                        issues_text = ", ".join(issues)
                        st.error(f"Trade #{trade_num}: {issues_text}")
    
    # Visualization - Compliance radar chart
    if metrics and len(metrics) > 3:
        st.markdown("---")
        st.markdown("### 📊 Compliance Radar Chart")
        
        categories = [k.replace('_', ' ').title() for k in metrics.keys()]
        scores = [v.get('score', 0) for v in metrics.values()]
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=scores,
            theta=categories,
            fill='toself',
            name='Your Compliance',
            line_color='#1f77b4'
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=[90] * len(categories),
            theta=categories,
            fill='toself',
            name='Target (90%)',
            line_color='#2ca02c',
            opacity=0.3
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            height=400
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)

def calculate_win_rate(total_trades, winning_trades):
    """Calculate win rate percentage"""
    if total_trades == 0:
        return 0
    return (winning_trades / total_trades) * 100

def calculate_rr_ratio(entry_price, exit_price, stop_loss, is_win):
    """Calculate Risk:Reward ratio"""
    try:
        entry = float(entry_price)
        exit_val = float(exit_price)
        sl = float(stop_loss)
        
        risk = abs(entry - sl)
        if risk == 0:
            return 0
        
        reward = abs(exit_val - entry)
        return reward / risk
    except:
        return 0

def format_rr_ratio(rr_value):
    """Format RR ratio as '1:X' trading format"""
    try:
        rr = float(rr_value)
        if rr == 0:
            return "0:0"
        return f"1:{rr:.2f}"
    except:
        return "N/A"

def get_dynamic_feedback(win_rate, total_trades):
    """Generate dynamic feedback based on win rate"""
    if total_trades < 10:
        return {
            'type': 'info',
            'title': '📊 Keep Building Your Track Record',
            'message': f"You have {total_trades} trades recorded. Aim for at least 20-30 trades to get meaningful statistics about your strategy's performance."
        }
    
    if win_rate < 30:
        return {
            'type': 'warning',
            'title': '⚠️ Strategy Needs Improvement',
            'message': f"Your current win rate of {win_rate:.1f}% suggests significant issues. Consider:\n\n"
                      "• **Review Your Entry Rules**: Are you entering too early or chasing moves?\n"
                      "• **Check Market Bias**: Are you fighting the trend?\n"
                      "• **Analyze Your Losses**: Look for patterns in your losing trades\n"
                      "• **Reduce Position Size**: Protect your capital while you refine your strategy\n"
                      "• **Paper Trade**: Test modifications without risking real money\n"
                      "• **Study Market Context**: Ensure you're trading in suitable market conditions"
        }
    elif win_rate < 40:
        return {
            'type': 'warning',
            'title': '🔍 Room for Improvement',
            'message': f"Your {win_rate:.1f}% win rate needs work. Focus on:\n\n"
                      "• **Discipline**: Are you following your rules consistently?\n"
                      "• **Entry Timing**: Fine-tune your entry signals\n"
                      "• **Risk Management**: Ensure proper stop-loss placement\n"
                      "• **Market Selection**: Trade only in favorable conditions\n"
                      "• **Review & Learn**: Analyze each trade to identify patterns"
        }
    elif win_rate < 50:
        return {
            'type': 'info',
            'title': '📈 You\'re Getting There',
            'message': f"A {win_rate:.1f}% win rate is approaching breakeven territory. To improve:\n\n"
                      "• **Optimize Your Risk:Reward**: Aim for 2:1 or better\n"
                      "• **Be More Selective**: Take only the highest probability setups\n"
                      "• **Follow Your Plan**: Stick to your entry and exit rules\n"
                      "• **Manage Emotions**: Avoid revenge trading after losses\n"
                      "• **Track Patterns**: Note which setups work best"
        }
    elif win_rate < 60:
        return {
            'type': 'success',
            'title': '✅ Solid Performance',
            'message': f"Your {win_rate:.1f}% win rate shows good strategy execution! To maintain and improve:\n\n"
                      "• **Stay Consistent**: Keep following your proven rules\n"
                      "• **Document Everything**: Record what works and why\n"
                      "• **Avoid Overtrading**: Quality over quantity\n"
                      "• **Protect Your Wins**: Use proper position sizing\n"
                      "• **Continue Learning**: Markets evolve, so should you"
        }
    elif win_rate < 70:
        return {
            'type': 'success',
            'title': '🌟 Excellent Trading',
            'message': f"Outstanding {win_rate:.1f}% win rate! You're doing great. Remember:\n\n"
                      "• **Avoid Overconfidence**: The market can humble anyone\n"
                      "• **Stick to Your Process**: Don't deviate from what works\n"
                      "• **Watch Position Sizing**: Don't risk too much on any single trade\n"
                      "• **Stay Humble**: Keep learning and adapting\n"
                      "• **Take Profits**: Don't let greed ruin good positions"
        }
    else:
        return {
            'type': 'success',
            'title': '🏆 Elite Performance',
            'message': f"Exceptional {win_rate:.1f}% win rate! This is elite-level trading. Critical reminders:\n\n"
                      "• **Beware of Overconfidence**: High win rates can breed complacency\n"
                      "• **Verify Data Quality**: Ensure all trades are logged accurately\n"
                      "• **Market Conditions**: Your strategy may be perfectly suited to current conditions\n"
                      "• **Stay Disciplined**: Success can lead to taking unnecessary risks\n"
                      "• **Plan for Drawdowns**: Even the best strategies have losing periods\n"
                      "• **Never Risk It All**: Protect your hard-earned profits"
        }

def calculate_performance_metrics(trades_df):
    """Calculate comprehensive performance metrics"""
    if len(trades_df) == 0:
        return None
    
    metrics = {}
    
    # Basic metrics
    total_trades = len(trades_df)
    wins = len(trades_df[trades_df['Result'] == 'Win'])
    losses = len(trades_df[trades_df['Result'] == 'Loss'])
    
    metrics['total_trades'] = total_trades
    metrics['wins'] = wins
    metrics['losses'] = losses
    metrics['win_rate'] = (wins / total_trades * 100) if total_trades > 0 else 0
    
    # Profit/Loss calculation
    trades_df['PnL'] = trades_df.apply(
        lambda row: (float(row['Exit Price']) - float(row['Entry Price'])) 
        if row['Result'] == 'Win' 
        else (float(row['Entry Price']) - float(row['Exit Price'])) * -1,
        axis=1
    )
    
    metrics['total_pnl'] = trades_df['PnL'].sum()
    metrics['avg_win'] = trades_df[trades_df['Result'] == 'Win']['PnL'].mean() if wins > 0 else 0
    metrics['avg_loss'] = trades_df[trades_df['Result'] == 'Loss']['PnL'].mean() if losses > 0 else 0
    metrics['avg_rr'] = trades_df['R:R Ratio'].mean()
    
    # Streaks
    current_streak = 0
    max_win_streak = 0
    max_loss_streak = 0
    current_streak_type = None
    
    for result in trades_df['Result']:
        if result == current_streak_type:
            current_streak += 1
        else:
            if current_streak_type == 'Win':
                max_win_streak = max(max_win_streak, current_streak)
            elif current_streak_type == 'Loss':
                max_loss_streak = max(max_loss_streak, current_streak)
            current_streak = 1
            current_streak_type = result
    
    # Final streak check
    if current_streak_type == 'Win':
        max_win_streak = max(max_win_streak, current_streak)
    elif current_streak_type == 'Loss':
        max_loss_streak = max(max_loss_streak, current_streak)
    
    metrics['max_win_streak'] = max_win_streak
    metrics['max_loss_streak'] = max_loss_streak
    
    # Profit factor
    total_wins_pnl = trades_df[trades_df['Result'] == 'Win']['PnL'].sum() if wins > 0 else 0
    total_losses_pnl = abs(trades_df[trades_df['Result'] == 'Loss']['PnL'].sum()) if losses > 0 else 0
    metrics['profit_factor'] = (total_wins_pnl / total_losses_pnl) if total_losses_pnl > 0 else 0
    
    return metrics

def calculate_consistency_score(trades_df, entry_rules, exit_rules):
    """Calculate how consistently trades follow the stated strategy"""
    if len(trades_df) == 0:
        return None
    
    # This is a simplified scoring system
    # In a real implementation, you'd need more sophisticated analysis
    
    score = 100
    factors = []
    
    # Check R:R consistency
    rr_ratios = trades_df['R:R Ratio'].dropna()
    if len(rr_ratios) > 0:
        rr_std = rr_ratios.std()
        if rr_std > 2:  # High variance in R:R ratios
            score -= 20
            factors.append("High variance in Risk:Reward ratios suggests inconsistent position sizing")
    
    # Check if stop-loss is consistently used
    missing_sl = trades_df['Stop-loss'].isna().sum()
    if missing_sl > 0:
        penalty = (missing_sl / len(trades_df)) * 30
        score -= penalty
        factors.append(f"{missing_sl} trades missing stop-loss data")
    
    # Check if take-profit is consistently used
    missing_tp = trades_df['Take-profit'].isna().sum()
    if missing_tp > 0:
        penalty = (missing_tp / len(trades_df)) * 20
        score -= penalty
        factors.append(f"{missing_tp} trades missing take-profit data")
    
    # Check trade timing consistency - STRICT RULE: Only 1 trade per day allowed
    overtrade_details = []
    if 'Date & Time' in trades_df.columns:
        trades_df['Date & Time'] = pd.to_datetime(trades_df['Date & Time'])
        trades_df = trades_df.sort_values('Date & Time').reset_index(drop=True)
        
        # Extract date only (ignore time)
        trades_df['Trade_Date'] = trades_df['Date & Time'].dt.date
        
        # Find dates with multiple trades
        date_counts = trades_df['Trade_Date'].value_counts()
        multiple_trade_dates = date_counts[date_counts > 1]
        
        if len(multiple_trade_dates) > 0:
            total_violations = (date_counts[date_counts > 1]).sum() - len(multiple_trade_dates)
            score -= min(30, total_violations * 3)  # Penalty up to 30 points
            
            # Collect details of all trades on days with multiple trades
            for trade_date in multiple_trade_dates.index:
                trades_on_date = trades_df[trades_df['Trade_Date'] == trade_date]
                trade_numbers = (trades_on_date.index + 1).tolist()
                trade_times = trades_on_date['Date & Time'].dt.strftime('%H:%M:%S').tolist()
                
                overtrade_details.append({
                    'date': trade_date.strftime('%Y-%m-%d'),
                    'trade_count': len(trades_on_date),
                    'trade_numbers': trade_numbers,
                    'trade_times': trade_times
                })
            
            factors.append(f"⚠️ OVERTRADING: {len(multiple_trade_dates)} days with multiple trades (Rule: Max 1 trade per day)")
    
    return {
        'score': max(0, score),
        'factors': factors,
        'overtrade_details': overtrade_details,
        'rating': 'Excellent' if score >= 80 else 'Good' if score >= 60 else 'Fair' if score >= 40 else 'Poor'
    }

def create_equity_curve(trades_df):
    """Create an equity curve chart"""
    if len(trades_df) == 0:
        return None
    
    # Sort by date
    trades_df = trades_df.sort_values('Date & Time')
    
    # Calculate cumulative PnL
    trades_df['Cumulative PnL'] = trades_df['PnL'].cumsum()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=trades_df['Date & Time'],
        y=trades_df['Cumulative PnL'],
        mode='lines+markers',
        name='Equity Curve',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=6)
    ))
    
    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    
    fig.update_layout(
        title='Equity Curve',
        xaxis_title='Date',
        yaxis_title='Cumulative P&L',
        hovermode='x unified',
        height=400
    )
    
    return fig

def create_daily_cumulative_pnl_chart(trades_df):
    """Create daily net cumulative P&L area chart"""
    if len(trades_df) == 0:
        return None
    
    # Sort by date
    trades_df_sorted = trades_df.sort_values('Date & Time').copy()
    
    # Calculate cumulative PnL
    trades_df_sorted['Cumulative PnL'] = trades_df_sorted['PnL'].cumsum()
    
    fig = go.Figure()
    
    # Separate positive and negative regions
    x_data = trades_df_sorted['Date & Time'].tolist()
    y_data = trades_df_sorted['Cumulative PnL'].tolist()
    
    # Create separate traces for positive and negative regions
    # First, add the positive area (green)
    x_positive = []
    y_positive = []
    
    for i in range(len(x_data)):
        if y_data[i] >= 0:
            x_positive.append(x_data[i])
            y_positive.append(y_data[i])
        else:
            # Add zero crossing point
            if x_positive:
                x_positive.append(x_data[i])
                y_positive.append(0)
                # Add the positive trace
                fig.add_trace(go.Scatter(
                    x=x_positive,
                    y=y_positive,
                    mode='lines',
                    line=dict(color='#2E7D32', width=2.5),
                    fill='tozeroy',
                    fillcolor='rgba(76, 175, 80, 0.4)',
                    showlegend=False,
                    hovertemplate='Date: %{x}<br>Cumulative P&L: $%{y:,.2f}<extra></extra>'
                ))
                x_positive = []
                y_positive = []
    
    # Add remaining positive segment
    if x_positive:
        fig.add_trace(go.Scatter(
            x=x_positive,
            y=y_positive,
            mode='lines',
            line=dict(color='#2E7D32', width=2.5),
            fill='tozeroy',
            fillcolor='rgba(76, 175, 80, 0.4)',
            showlegend=False,
            hovertemplate='Date: %{x}<br>Cumulative P&L: $%{y:,.2f}<extra></extra>'
        ))
    
    # Now add the negative area (red)
    x_negative = []
    y_negative = []
    
    for i in range(len(x_data)):
        if y_data[i] < 0:
            x_negative.append(x_data[i])
            y_negative.append(y_data[i])
        else:
            # Add zero crossing point
            if x_negative:
                x_negative.append(x_data[i])
                y_negative.append(0)
                # Add the negative trace
                fig.add_trace(go.Scatter(
                    x=x_negative,
                    y=y_negative,
                    mode='lines',
                    line=dict(color='#C62828', width=2.5),
                    fill='tozeroy',
                    fillcolor='rgba(244, 67, 54, 0.4)',
                    showlegend=False,
                    hovertemplate='Date: %{x}<br>Cumulative P&L: $%{y:,.2f}<extra></extra>'
                ))
                x_negative = []
                y_negative = []
    
    # Add remaining negative segment
    if x_negative:
        fig.add_trace(go.Scatter(
            x=x_negative,
            y=y_negative,
            mode='lines',
            line=dict(color='#C62828', width=2.5),
            fill='tozeroy',
            fillcolor='rgba(244, 67, 54, 0.4)',
            showlegend=False,
            hovertemplate='Date: %{x}<br>Cumulative P&L: $%{y:,.2f}<extra></extra>'
        ))
    
    # Add the main line on top for smooth appearance
    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        mode='lines',
        line=dict(color='#1565C0', width=2.5),
        showlegend=False,
        hovertemplate='Date: %{x}<br>Cumulative P&L: $%{y:,.2f}<extra></extra>'
    ))
    
    # Add zero line
    fig.add_hline(y=0, line_dash="solid", line_color="rgba(128, 128, 128, 0.4)", line_width=1)
    
    fig.update_layout(
        title='DAILY NET CUMULATIVE P&L   (ALL DATES)',
        xaxis_title='',
        yaxis_title='',
        hovermode='x unified',
        height=400,
        showlegend=False,
        plot_bgcolor='white',
        yaxis=dict(tickformat='$,.2f', gridcolor='#f0f0f0'),
        xaxis=dict(gridcolor='#f0f0f0')
    )
    
    return fig

def create_net_daily_pnl_chart(trades_df):
    """Create net daily P&L bar chart"""
    if len(trades_df) == 0:
        return None
    
    # Convert Date & Time to date only and group by date
    trades_df_copy = trades_df.copy()
    trades_df_copy['Date'] = pd.to_datetime(trades_df_copy['Date & Time']).dt.date
    
    # Group by date and sum PnL
    daily_pnl = trades_df_copy.groupby('Date')['PnL'].sum().reset_index()
    daily_pnl = daily_pnl.sort_values('Date')
    
    # Determine colors
    colors = ['#00CC96' if pnl >= 0 else '#EF553B' for pnl in daily_pnl['PnL']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=daily_pnl['Date'],
        y=daily_pnl['PnL'],
        marker_color=colors,
        hovertemplate='Date: %{x}<br>Net P&L: $%{y:,.2f}<extra></extra>',
        showlegend=False
    ))
    
    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray", line_width=1.5, opacity=0.7)
    
    fig.update_layout(
        title='NET DAILY P&L   (ALL DATES)',
        xaxis_title='',
        yaxis_title='',
        hovermode='x unified',
        height=400,
        plot_bgcolor='white',
        yaxis=dict(tickformat='$,.2f', gridcolor='#f0f0f0'),
        xaxis=dict(gridcolor='#f0f0f0')
    )
    
    return fig

def create_trade_distribution_by_day_chart(trades_df):
    """Create trade distribution by day of week horizontal bar chart"""
    if len(trades_df) == 0:
        return None
    
    # Extract day of week
    trades_df_copy = trades_df.copy()
    trades_df_copy['Date'] = pd.to_datetime(trades_df_copy['Date & Time'])
    trades_df_copy['DayOfWeek'] = trades_df_copy['Date'].dt.day_name()
    
    # Define day order
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Count trades by day
    day_counts = trades_df_copy['DayOfWeek'].value_counts()
    day_counts = day_counts.reindex(day_order, fill_value=0)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=day_counts.index,
        x=day_counts.values,
        orientation='h',
        marker_color='#5B5FC7',
        hovertemplate='%{y}: %{x} trades<extra></extra>',
        showlegend=False
    ))
    
    fig.update_layout(
        title='TRADE DISTRIBUTION BY DAY OF THE WEEK<br>(ALL DATES)',
        xaxis_title='',
        yaxis_title='',
        height=400,
        plot_bgcolor='white',
        xaxis=dict(gridcolor='#f0f0f0'),
        yaxis=dict(categoryorder='array', categoryarray=day_order[::-1])
    )
    
    return fig

def create_performance_by_day_chart(trades_df):
    """Create performance by day of week horizontal bar chart"""
    if len(trades_df) == 0:
        return None
    
    # Extract day of week
    trades_df_copy = trades_df.copy()
    trades_df_copy['Date'] = pd.to_datetime(trades_df_copy['Date & Time'])
    trades_df_copy['DayOfWeek'] = trades_df_copy['Date'].dt.day_name()
    
    # Define day order
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Sum PnL by day
    day_performance = trades_df_copy.groupby('DayOfWeek')['PnL'].sum()
    day_performance = day_performance.reindex(day_order, fill_value=0)
    
    # Determine colors
    colors = ['#00CC96' if pnl >= 0 else '#EF553B' for pnl in day_performance.values]
    
    # Create hover text with values
    hover_text = [f'{day}: ${pnl:,.2f}' for day, pnl in zip(day_performance.index, day_performance.values)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=day_performance.index,
        x=day_performance.values,
        orientation='h',
        marker_color=colors,
        text=[f'${pnl:,.2f}' if pnl != 0 else '' for pnl in day_performance.values],
        textposition='outside',
        hovertemplate='%{y}: $%{x:,.2f}<extra></extra>',
        showlegend=False
    ))
    
    # Add zero line
    fig.add_vline(x=0, line_dash="solid", line_color="black", line_width=1.5, opacity=0.7)
    
    fig.update_layout(
        title='PERFORMANCE BY DAY OF THE WEEK<br>(ALL DATES)',
        xaxis_title='',
        yaxis_title='',
        height=400,
        plot_bgcolor='white',
        xaxis=dict(tickformat='$,.2f', gridcolor='#f0f0f0'),
        yaxis=dict(categoryorder='array', categoryarray=day_order[::-1])
    )
    
    return fig

def generate_example_strategies_with_gemini(api_key):
    """Generate 2 basic example strategies using Gemini"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        prompt = """Generate 2 VERY SIMPLE trading strategies that a complete beginner with NO technical knowledge can understand and implement. 

For each strategy, provide:

**Strategy Name:** [Creative but professional name]

**Instrument:** [Suitable instrument like BTC-USD, AAPL, SPY, etc.]

**Strategy Description:** [2-3 sentences explaining the overall approach in simple language]

**Entry Rules:**
[Clear bullet points with specific conditions for entering a trade]

**Exit Rules:**
[Clear bullet points with specific conditions for exiting a trade]

**Stop-Loss Rules:**
[Specific stop-loss placement rules with concrete examples]

**Take-Profit Rules:**
[Specific take-profit placement rules with concrete examples]

**Time Window:** [Recommended trading session like "Asia Session", "London Session", "New York Session", or "None - Trade Anytime"]

---

CRITICAL REQUIREMENTS:
- DO NOT use ANY technical indicators (NO RSI, MACD, EMA, SMA, Bollinger Bands, etc.)
- DO NOT use complex chart patterns or jargon
- DO NOT use mathematical formulas, variables, or expressions
- Use ONLY concrete numbers in examples (like "100 dollars" or "5 percent" - write it out clearly)
- Focus ONLY on simple concepts:
  * Price going up or down
  * Previous high or low prices
  * Round numbers like 100, 1000, 50000
  * Green candles (price went up) or red candles (price went down)
  * Fixed dollar amounts for profit and loss
  * Simple percentage changes (write as "3 percent" not "3%")
  * Time-based rules (write as "24 hours" not "24h")

FORMATTING RULES:
- Use simple bullet points with dashes (-)
- Write all numbers clearly with spaces
- Use full words, not symbols or abbreviations
- Keep sentences short and clear
- Each bullet point should be one simple rule
- Always use concrete example numbers

EXAMPLE OF GOOD SIMPLE CONCEPTS:
- "Buy when the price drops by 50 dollars from yesterday's closing price"
- "Sell when you make 100 dollars profit"
- "Place your stop-loss 20 dollars below your entry price"
- "Exit the trade after two red candles in a row"
- "Buy when price goes above yesterday's highest price"

Generate 2 SIMPLE strategies now with CLEAR, READABLE text:"""
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating strategies: {str(e)}"

# Main UI
st.title("📊 Strategy Developer & Winning Rate")
st.markdown("**Develop, track, and analyze your trading strategy with AI-powered insights**")

# Sidebar for Groq API Key
with st.sidebar:
    st.subheader("🔑 Groq API Configuration")
    groq_api_input = st.text_input(
        "Groq API Key",
        value=st.session_state.groq_api_key,
        type="password",
        help="Enter your Groq API key for strategy rephrasing"
    )
    if groq_api_input != st.session_state.groq_api_key:
        st.session_state.groq_api_key = groq_api_input
    
    # Keep Gemini for chart analysis
    st.subheader("🔑 Gemini API Configuration")
    api_key_input = st.text_input(
        "Gemini API Key",
        value=st.session_state.gemini_api_key,
        type="password",
        help="Enter your Gemini API key for chart analysis"
    )
    if api_key_input != st.session_state.gemini_api_key:
        st.session_state.gemini_api_key = api_key_input
    
    st.markdown("---")
    st.markdown("### 📖 Quick Guide")
    st.markdown("""
    1. Select your instrument
    2. Define your strategy rules
    3. Upload chart for AI analysis
    4. Log your trades
    5. Review performance metrics
    """)

# Main content area with tabs
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Strategy Setup", "📊 Trade Logging", "📈 Performance Analytics", "🤖 AI Analysis"])

# TAB 1: Strategy Setup
with tab1:
    # Check if user knows how to build a strategy
    if st.session_state.knows_strategy_building is None:
        st.header("🤔 Before We Begin...")
        st.markdown("### Do you know how to build a trading strategy?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Yes, I know", type="primary", use_container_width=True):
                st.session_state.knows_strategy_building = True
                st.session_state.show_strategy_setup = True
                st.rerun()
        
        with col2:
            if st.button("❌ No, I need help", type="secondary", use_container_width=True):
                st.session_state.knows_strategy_building = False
                st.session_state.show_strategy_setup = False
                st.rerun()
        
        st.markdown("---")
        st.info("💡 **Tip:** Choose honestly! If you're new to trading strategies, we'll provide educational resources and examples to help you get started.")
    
    # If user doesn't know how to build a strategy
    elif st.session_state.knows_strategy_building == False:
        st.header("📚 Learn About Trading Strategies")
        
        st.markdown("""
        ### Welcome to Strategy Development! 🎓
        
        A trading strategy is a set of rules that define when to enter and exit trades. Before building your own, 
        it's important to understand the fundamentals. Here are some resources to help you get started:
        """)
        
        st.markdown("---")
        
        # Educational Videos Section
        st.subheader("🎥 Watch These Educational Videos")
        st.markdown("These videos will teach you the basics of trading strategies:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📺 Video 1: Trading Strategy Fundamentals")
            hls_player(VIDEO_1_URL, "strategy_video1", height=400)
            st.caption("Learn the basics of what makes a good trading strategy")
        
        with col2:
            st.markdown("#### 📺 Video 2: Building Your First Strategy")
            hls_player(VIDEO_2_URL, "strategy_video2", height=400)
            st.caption("Step-by-step guide to developing your trading strategy")
        
        st.markdown("---")
        
        # AI Generated Example Strategies Section
        st.subheader("🤖 AI-Generated Example Strategies")
        st.markdown("Let our AI create 2 simple example strategies to help you understand the structure:")
        
        if st.button("🚀 Generate Example Strategies with Gemini", type="primary"):
            if not st.session_state.gemini_api_key:
                st.error("⚠️ Please enter your Gemini API key in the sidebar first!")
            else:
                with st.spinner("🔄 Generating example strategies... This may take a moment."):
                    example_strategies = generate_example_strategies_with_gemini(st.session_state.gemini_api_key)
                    
                    if example_strategies and not example_strategies.startswith("Error"):
                        st.success("✅ Example strategies generated successfully!")
                        st.markdown("---")
                        st.markdown(example_strategies)
                    else:
                        st.error(f"❌ {example_strategies}")
        
        st.markdown("---")
        
        # Option to proceed after learning
        st.subheader("📝 Ready to Build Your Own Strategy?")
        st.markdown("Once you've watched the videos and reviewed the examples, you can proceed to build your own strategy.")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            if st.button("✅ I'm Ready! Show Me the Setup", type="primary", use_container_width=True):
                st.session_state.knows_strategy_building = True
                st.session_state.show_strategy_setup = True
                st.rerun()
        
        st.markdown("---")
        st.info("💡 **Tip:** Take your time to learn! Building a solid strategy foundation is crucial for trading success.")
    
    # If user knows how to build a strategy OR has completed learning
    elif st.session_state.knows_strategy_building == True or st.session_state.show_strategy_setup == True:
        st.header("1️⃣ Instrument & Strategy Definition")
    
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📍 Instrument Selection")
            
            # Instrument input with validation
            instrument_input = st.text_input(
                "Enter Instrument Name",
                value=st.session_state.strategy_data['instrument'] or '',
                help="e.g., EUR/USD, GBP/USD, USD/JPY, BTC/USDT, GOLD, AAPL",
                key='instrument_input'
            )
            
            if st.button("Load/Create Strategy", type="primary"):
                if instrument_input:
                    instrument_input = instrument_input.strip().upper()
                    # Try to load existing data
                    loaded_data = load_strategy_data(instrument_input)
                    if loaded_data:
                        st.session_state.strategy_data = loaded_data
                        st.success(f"✅ Loaded existing strategy for {instrument_input}")
                    else:
                        st.session_state.strategy_data['instrument'] = instrument_input
                        st.success(f"✅ Created new strategy for {instrument_input}")
                    st.rerun()
                else:
                    st.error("Please enter an instrument name")
            
            # Recommended pairs info box - placed after button
            with st.expander("💡 Recommended Pairs for Beginners", expanded=False):
                st.markdown("""
                **Most Liquid & Beginner-Friendly:**
                
                - **EUR/USD** (Euro/US Dollar)
                - **USD/JPY** (US Dollar/Japanese Yen)
                - **GBP/USD** (British Pound/US Dollar)
                
                **Why these pairs?**
                - ✅ Highly liquid markets
                - ✅ Easier for beginners
                - ✅ Simple, predictable chart patterns
                - ✅ Lower spreads & better execution
                """)
            
            if st.session_state.strategy_data['instrument']:
                st.info(f"**Current Instrument:** {st.session_state.strategy_data['instrument']}")
                st.caption("⚠️ All trades must belong to this instrument")
        
        with col2:
            st.subheader("📝 Strategy Description")
            strategy_desc = st.text_area(
                "Describe your trading strategy",
                value=st.session_state.strategy_data.get('strategy_description', ''),
                height=150,
                help="Explain your overall approach, market conditions, timeframe, etc.",
                key='strategy_description_input'
            )
            if strategy_desc != st.session_state.strategy_data.get('strategy_description', ''):
                st.session_state.strategy_data['strategy_description'] = strategy_desc
                if st.session_state.strategy_data['instrument']:
                    save_strategy_data()
        
        st.markdown("---")
        
        # Time Window / Trading Session Selection
        st.header("🕐 Trading Time Window")
        st.markdown("Select your preferred trading session based on market activity.")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            time_window_options = {
                "None - Trade Anytime": None,
                "Asia Session (1:30 AM - 2:30 PM)": "Asia Session (1:30 AM - 2:30 PM)",
                "London Session (12:30 PM - 3:00 PM)": "London Session (12:30 PM - 3:00 PM)",
                "New York Session (6:30 PM - 10:30 PM)": "New York Session (6:30 PM - 10:30 PM)"
            }
            
            current_selection = st.session_state.strategy_data.get('time_window', None)
            # Find the key for the current selection
            current_key = "None - Trade Anytime"
            for key, value in time_window_options.items():
                if value == current_selection:
                    current_key = key
                    break
            
            selected_window = st.selectbox(
                "Select Trading Session",
                options=list(time_window_options.keys()),
                index=list(time_window_options.keys()).index(current_key),
                help="Choose the market session that aligns with your strategy",
                key='time_window_select'
            )
            
            selected_value = time_window_options[selected_window]
            if selected_value != st.session_state.strategy_data.get('time_window', None):
                st.session_state.strategy_data['time_window'] = selected_value
                if st.session_state.strategy_data['instrument']:
                    save_strategy_data()
        
        with col2:
            st.markdown("""  
            **Session Info:**
            
            🌏 **Asia (1:30 AM - 2:30 PM)**  
            Low-medium volatility, steady trends
            
            🇬🇧 **London (12:30 PM - 3:00 PM)**  
            Peak volume & volatility period  
            ⚠️ After 3 PM: Market gets dry
            
            🇺🇸 **New York (6:30 PM - 10:30 PM)**  
            High volume (2nd hour onwards)  
            ⚠️ After 10:30 PM: Market becomes flat
            
            💡 **Tip:** Trade during peak hours for best results
            
            *All times in IST (Indian Standard Time)*
            """)
        
        st.caption("📊 Source: [Forex Market Hours - BabyPips](https://www.babypips.com/tools/forex-market-hours)")
        
        st.markdown("---")
        st.header("2️⃣ Trade System Components")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📥 Entry Rules")
            entry_rules = st.text_area(
                "Define your entry conditions",
                value=st.session_state.strategy_data.get('entry_rules', ''),
                height=150,
                help="Be specific: indicators, price action, patterns, etc.",
                key='entry_rules_input'
            )
            if entry_rules != st.session_state.strategy_data.get('entry_rules', ''):
                st.session_state.strategy_data['entry_rules'] = entry_rules
                if st.session_state.strategy_data['instrument']:
                    save_strategy_data()
            
            st.subheader("🛑 Stop-Loss Rules")
            stop_loss_rules = st.text_area(
                "Define your stop-loss placement",
                value=st.session_state.strategy_data.get('stop_loss', ''),
                height=100,
                help="How and where you place stop-losses",
                key='stop_loss_input'
            )
            if stop_loss_rules != st.session_state.strategy_data.get('stop_loss', ''):
                st.session_state.strategy_data['stop_loss'] = stop_loss_rules
                if st.session_state.strategy_data['instrument']:
                    save_strategy_data()
        
        with col2:
            st.subheader("📤 Exit Rules")
            exit_rules = st.text_area(
                "Define your exit conditions",
                value=st.session_state.strategy_data.get('exit_rules', ''),
                height=150,
                help="When and how you exit trades (profit or loss)",
                key='exit_rules_input'
            )
            if exit_rules != st.session_state.strategy_data.get('exit_rules', ''):
                st.session_state.strategy_data['exit_rules'] = exit_rules
                if st.session_state.strategy_data['instrument']:
                    save_strategy_data()
            
            st.subheader("🎯 Take-Profit Rules")
            take_profit_rules = st.text_area(
                "Define your take-profit strategy",
                value=st.session_state.strategy_data.get('take_profit', ''),
                height=100,
                help="How you lock in profits (fixed target, trailing, etc.)",
                key='take_profit_input'
            )
            if take_profit_rules != st.session_state.strategy_data.get('take_profit', ''):
                st.session_state.strategy_data['take_profit'] = take_profit_rules
                if st.session_state.strategy_data['instrument']:
                    save_strategy_data()
        
        # Analyze button section
        st.markdown("---")
        st.header("🤖 AI-Powered Strategy Rephrasing")
        st.markdown("Use Groq AI to rephrase and grammatically correct your strategy inputs without changing their meaning.")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info("💡 The AI will only fix grammar and sentence structure - it won't add or remove your content.")
        with col2:
            if st.button("✨ Analyze", type="primary", use_container_width=True):
                if not st.session_state.groq_api_key:
                    st.error("❌ Please enter your Groq API Key in the sidebar first!")
                elif not st.session_state.strategy_data['instrument']:
                    st.error("❌ Please enter an instrument name first!")
                else:
                    # Check if user has entered any strategy content
                    has_content = any([
                        st.session_state.strategy_data.get('strategy_description', ''),
                        st.session_state.strategy_data.get('entry_rules', ''),
                        st.session_state.strategy_data.get('exit_rules', ''),
                        st.session_state.strategy_data.get('stop_loss', ''),
                        st.session_state.strategy_data.get('take_profit', '')
                    ])
                    
                    if not has_content:
                        st.warning("⚠️ Please enter at least one strategy component before analyzing.")
                    else:
                        with st.spinner("🔄 Analyzing and rephrasing your strategy..."):
                            rephrased = rephrase_strategy_with_groq(
                                instrument=st.session_state.strategy_data.get('instrument', ''),
                                strategy_description=st.session_state.strategy_data.get('strategy_description', ''),
                                entry_rules=st.session_state.strategy_data.get('entry_rules', ''),
                                exit_rules=st.session_state.strategy_data.get('exit_rules', ''),
                                stop_loss=st.session_state.strategy_data.get('stop_loss', ''),
                                take_profit=st.session_state.strategy_data.get('take_profit', ''),
                                api_key=st.session_state.groq_api_key
                            )
                            st.session_state.rephrased_content = rephrased
                            st.success("✅ Analysis complete! Review the rephrased version below.")
        
        # Display rephrased content if available
        if st.session_state.rephrased_content:
            st.markdown("---")
            st.subheader("📝 Rephrased Strategy")
            
            with st.expander("🔍 View Rephrased Content", expanded=True):
                st.markdown(st.session_state.rephrased_content)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📋 Copy to Clipboard"):
                        st.code(st.session_state.rephrased_content, language=None)
                        st.info("💡 Select and copy the text from the code block above")
                with col2:
                    if st.button("🗑️ Clear Rephrased Content"):
                        st.session_state.rephrased_content = None
                        st.rerun()

# TAB 2: Trade Logging
with tab2:
    st.header("📊 Trade Log Management")
    
    if not st.session_state.strategy_data['instrument']:
        st.warning("⚠️ Please select an instrument in the Strategy Setup tab first")
    else:
        # Quick Stats Input
        st.subheader("⚡ Quick Trade Statistics")
        col1, col2, col3 = st.columns(3)
        
        # Calculate current stats from logged trades
        current_trades = len(st.session_state.strategy_data['trades'])
        current_wins = len([t for t in st.session_state.strategy_data['trades'] if t.get('result') == 'Win'])
        current_losses = len([t for t in st.session_state.strategy_data['trades'] if t.get('result') == 'Loss'])
        
        with col1:
            total_trades_input = st.number_input(
                "Total Trades",
                min_value=0,
                value=current_trades,
                help="Total number of trades taken"
            )
        
        with col2:
            winning_trades_input = st.number_input(
                "Winning Trades",
                min_value=0,
                max_value=total_trades_input,
                value=min(current_wins, total_trades_input),
                help="Number of profitable trades"
            )
        
        with col3:
            losing_trades_input = st.number_input(
                "Losing Trades",
                min_value=0,
                max_value=total_trades_input,
                value=min(current_losses, total_trades_input),
                help="Number of losing trades"
            )
        
        # Win Rate Display
        if total_trades_input > 0:
            win_rate = calculate_win_rate(total_trades_input, winning_trades_input)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Win Rate", f"{win_rate:.2f}%")
            with col2:
                st.metric("Risk/Reward Needed", f"{(100-win_rate)/win_rate:.2f}:1" if win_rate > 0 else "N/A")
            with col3:
                breakeven_wr = 50
                delta = win_rate - breakeven_wr
                st.metric("vs Breakeven (50%)", f"{delta:+.1f}%")
            
            # Dynamic Feedback
            feedback = get_dynamic_feedback(win_rate, total_trades_input)
            if feedback['type'] == 'success':
                st.success(f"**{feedback['title']}**\n\n{feedback['message']}")
            elif feedback['type'] == 'warning':
                st.warning(f"**{feedback['title']}**\n\n{feedback['message']}")
            else:
                st.info(f"**{feedback['title']}**\n\n{feedback['message']}")
        
        st.markdown("---")
        
        # CSV Upload Section
        with st.expander("📤 Import Trades from CSV", expanded=False):
            st.subheader("Upload Your Trade History")
            st.markdown("""
            **CSV Format Requirements:**
            - Required columns: `Date & Time`, `Entry Price`, `Exit Price`, `Result` (Win/Loss)
            - Optional columns: `Stop-loss`, `Take-profit`, `Notes`, `Strategy Name`
            - Date format: YYYY-MM-DD HH:MM or YYYY-MM-DD
            """)
            
            # Show example format
            if st.checkbox("Show Example CSV Format"):
                example_data = {
                    'Date & Time': ['2024-11-01 10:30', '2024-11-02 14:15', '2024-11-03 09:00'],
                    'Entry Price': [50000.00, 50500.00, 49800.00],
                    'Exit Price': [51000.00, 50300.00, 50200.00],
                    'Stop-loss': [49500.00, 50200.00, 49500.00],
                    'Take-profit': [51500.00, 51000.00, 50500.00],
                    'Result': ['Win', 'Loss', 'Win'],
                    'Notes': ['Good entry', 'Stopped out', 'Perfect setup'],
                    'Strategy Name': ['Breakout', 'Breakout', 'Breakout']
                }
                st.dataframe(pd.DataFrame(example_data), use_container_width=True)
            
            uploaded_csv = st.file_uploader(
                "Choose a CSV file",
                type=['csv'],
                help="Upload a CSV file with your trade history",
                key='csv_uploader'
            )
            
            if uploaded_csv is not None:
                try:
                    # Read the CSV
                    df = pd.read_csv(uploaded_csv)
                    
                    # Display preview
                    st.write("**Preview of uploaded data:**")
                    st.dataframe(df.head(10), use_container_width=True)
                    
                    # Validate required columns
                    required_cols = ['Date & Time', 'Entry Price', 'Exit Price', 'Result']
                    missing_cols = [col for col in required_cols if col not in df.columns]
                    
                    if missing_cols:
                        st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
                    else:
                        st.success(f"✅ Found {len(df)} trades in the CSV file")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            append_mode = st.radio(
                                "Import Mode:",
                                ["Append to existing trades", "Replace all trades"],
                                help="Choose whether to add to current trades or replace them"
                            )
                        
                        with col2:
                            st.write("")
                            st.write("")
                            if st.button("📥 Import Trades", type="primary"):
                                imported_count = 0
                                errors = []
                                
                                # Clear existing trades if replace mode
                                if append_mode == "Replace all trades":
                                    st.session_state.strategy_data['trades'] = []
                                
                                # Process each row
                                for idx, row in df.iterrows():
                                    try:
                                        # Parse date/time
                                        try:
                                            trade_datetime = pd.to_datetime(row['Date & Time'])
                                        except:
                                            trade_datetime = datetime.now()
                                        
                                        # Get required fields
                                        entry_price = float(row['Entry Price'])
                                        exit_price = float(row['Exit Price'])
                                        result = str(row['Result']).strip()
                                        
                                        # Validate result
                                        if result not in ['Win', 'Loss']:
                                            errors.append(f"Row {idx+2}: Invalid result '{result}' (must be 'Win' or 'Loss')")
                                            continue
                                        
                                        # Get optional fields - handle multiple column name variations
                                        stop_loss_col = None
                                        for col in ['Stop-loss', 'Stop-Loss', 'Stop_Loss', 'Stop Loss', 'Stoploss']:
                                            if col in row.index:
                                                stop_loss_col = col
                                                break
                                        stop_loss = float(row[stop_loss_col]) if stop_loss_col and pd.notna(row.get(stop_loss_col, 0)) else 0
                                        
                                        take_profit_col = None
                                        for col in ['Take-profit', 'Take-Profit', 'Take_Profit', 'Take Profit', 'Takeprofit']:
                                            if col in row.index:
                                                take_profit_col = col
                                                break
                                        take_profit = float(row[take_profit_col]) if take_profit_col and pd.notna(row.get(take_profit_col, 0)) else 0
                                        
                                        notes = str(row.get('Notes', '')) if pd.notna(row.get('Notes', '')) else ''
                                        strategy_name = str(row.get('Strategy Name', '')) if pd.notna(row.get('Strategy Name', '')) else ''
                                        
                                        # Calculate R:R ratio
                                        rr_ratio = calculate_rr_ratio(entry_price, exit_price, stop_loss, result == 'Win')
                                        
                                        # Create trade record
                                        trade_record = {
                                            'date_time': trade_datetime,
                                            'instrument': st.session_state.strategy_data['instrument'],
                                            'entry_price': entry_price,
                                            'exit_price': exit_price,
                                            'stop_loss': stop_loss,
                                            'take_profit': take_profit,
                                            'rr_ratio': rr_ratio,
                                            'result': result,
                                            'notes': notes,
                                            'strategy_name': strategy_name
                                        }
                                        
                                        st.session_state.strategy_data['trades'].append(trade_record)
                                        imported_count += 1
                                        
                                    except Exception as e:
                                        errors.append(f"Row {idx+2}: {str(e)}")
                                
                                # Save and show results
                                save_strategy_data()
                                
                                if imported_count > 0:
                                    st.success(f"✅ Successfully imported {imported_count} trades!")
                                
                                if errors:
                                    with st.expander(f"⚠️ {len(errors)} errors occurred", expanded=False):
                                        for error in errors[:10]:  # Show first 10 errors
                                            st.error(error)
                                        if len(errors) > 10:
                                            st.info(f"... and {len(errors) - 10} more errors")
                                
                                st.rerun()
                
                except Exception as e:
                    st.error(f"❌ Error reading CSV file: {str(e)}")
        
        st.markdown("---")
        
        # Add New Trade
        with st.expander("➕ Add New Trade", expanded=False):
            st.subheader("Log a New Trade")
            
            col1, col2 = st.columns(2)
            
            with col1:
                trade_date = st.date_input("Trade Date", value=date.today())
                trade_time = st.time_input("Trade Time", value=datetime.now().time())
                entry_price = st.number_input("Entry Price", min_value=0.0, format="%.4f")
                exit_price = st.number_input("Exit Price", min_value=0.0, format="%.4f")
                stop_loss_price = st.number_input("Stop-Loss Price", min_value=0.0, format="%.4f")
            
            with col2:
                take_profit_price = st.number_input("Take-Profit Price", min_value=0.0, format="%.4f")
                trade_result = st.selectbox("Result", ["Win", "Loss"])
                strategy_name = st.text_input("Strategy Name", value=st.session_state.strategy_data.get('strategy_description', '')[:50])
                trade_notes = st.text_area("Trade Notes", help="Any observations about this trade")
            
            if st.button("💾 Save Trade", type="primary"):
                if entry_price > 0 and exit_price > 0:
                    # Calculate R:R ratio
                    rr_ratio = calculate_rr_ratio(entry_price, exit_price, stop_loss_price, trade_result == 'Win')
                    
                    # Create trade record
                    trade_record = {
                        'date_time': datetime.combine(trade_date, trade_time),
                        'instrument': st.session_state.strategy_data['instrument'],
                        'entry_price': entry_price,
                        'exit_price': exit_price,
                        'stop_loss': stop_loss_price,
                        'take_profit': take_profit_price,
                        'rr_ratio': rr_ratio,
                        'result': trade_result,
                        'notes': trade_notes,
                        'strategy_name': strategy_name
                    }
                    
                    st.session_state.strategy_data['trades'].append(trade_record)
                    save_strategy_data()
                    st.success("✅ Trade logged successfully!")
                    st.rerun()
                else:
                    st.error("Please enter valid entry and exit prices")
        
        st.markdown("---")
        
        # Display Trade Log Table
        st.subheader("📋 Trade History")
        
        if st.session_state.strategy_data['trades']:
            # Convert to DataFrame
            trades_df = pd.DataFrame(st.session_state.strategy_data['trades'])
            
            # Rename columns for display
            display_df = trades_df.copy()
            display_df.columns = ['Date & Time', 'Instrument', 'Entry Price', 'Exit Price', 
                                   'Stop-loss', 'Take-profit', 'R:R Ratio', 'Result', 'Notes', 'Strategy Name']
            
            # Format columns
            display_df['Date & Time'] = pd.to_datetime(display_df['Date & Time']).dt.strftime('%Y-%m-%d %H:%M')
            display_df['Entry Price'] = display_df['Entry Price'].apply(lambda x: f"{x:.4f}")
            display_df['Exit Price'] = display_df['Exit Price'].apply(lambda x: f"{x:.4f}")
            display_df['Stop-loss'] = display_df['Stop-loss'].apply(lambda x: f"{x:.4f}" if x > 0 else "N/A")
            display_df['Take-profit'] = display_df['Take-profit'].apply(lambda x: f"{x:.4f}" if x > 0 else "N/A")
            display_df['R:R Ratio'] = display_df['R:R Ratio'].apply(format_rr_ratio)
            
            # Display with styling
            st.dataframe(
                display_df,
                use_container_width=True,
                height=400
            )
            
            # Export options
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                csv = display_df.to_csv(index=False)
                st.download_button(
                    label="📥 Export to CSV",
                    data=csv,
                    file_name=f"{st.session_state.strategy_data['instrument']}_trades_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                if st.button("🗑️ Clear All Trades"):
                    if st.session_state.get('confirm_clear', False):
                        st.session_state.strategy_data['trades'] = []
                        save_strategy_data()
                        st.session_state.confirm_clear = False
                        st.success("All trades cleared")
                        st.rerun()
                    else:
                        st.session_state.confirm_clear = True
                        st.warning("Click again to confirm deletion")
            
            # Strategy Compliance Analysis Section
            st.markdown("---")
            st.header("🤖 AI Strategy Compliance Check")
            st.markdown("Analyze if your recent trades are following your defined strategy rules.")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.info("💡 AI will check your trades for compliance with instrument, time window, risk management, and strategy rules.")
            with col2:
                if st.button("🔍 Analyze Compliance", type="primary", use_container_width=True):
                    if not st.session_state.gemini_api_key:
                        st.error("❌ Please enter your Gemini API Key in the sidebar first!")
                    elif len(st.session_state.strategy_data['trades']) == 0:
                        st.warning("⚠️ No trades available to analyze. Please add some trades first.")
                    else:
                        # Check if strategy is defined
                        has_strategy = any([
                            st.session_state.strategy_data.get('strategy_description', ''),
                            st.session_state.strategy_data.get('entry_rules', ''),
                            st.session_state.strategy_data.get('exit_rules', ''),
                        ])
                        
                        if not has_strategy:
                            st.warning("⚠️ Please define your strategy in the Strategy Setup tab first for better analysis.")
                        else:
                            with st.spinner("🔄 Analyzing your trades for strategy compliance..."):
                                compliance_result = analyze_strategy_compliance_with_gemini(
                                    strategy_data=st.session_state.strategy_data,
                                    trades=st.session_state.strategy_data['trades'],
                                    api_key=st.session_state.gemini_api_key
                                )
                                st.session_state.compliance_analysis = compliance_result
                                st.success("✅ Compliance analysis complete! Review the results below.")
            
            # Display compliance analysis results
            if st.session_state.compliance_analysis:
                st.markdown("---")
                display_compliance_dashboard(st.session_state.compliance_analysis)
                
                # Action buttons
                col1, col2, col3 = st.columns([2, 1, 1])
                with col2:
                    if st.button("🔄 Re-analyze"):
                        st.session_state.compliance_analysis = None
                        st.rerun()
                with col3:
                    if st.button("🗑️ Clear Dashboard"):
                        st.session_state.compliance_analysis = None
                        st.rerun()
        else:
            st.info("No trades logged yet. Use the form above to add your first trade.")

# TAB 3: Performance Analytics
with tab3:
    st.header("📈 Performance Analytics Dashboard")
    
    if not st.session_state.strategy_data['instrument']:
        st.warning("⚠️ Please select an instrument in the Strategy Setup tab first")
    elif not st.session_state.strategy_data['trades']:
        st.info("📊 No trades logged yet. Add trades in the Trade Logging tab to see analytics.")
    else:
        # Convert trades to DataFrame
        trades_df = pd.DataFrame(st.session_state.strategy_data['trades'])
        trades_df.columns = ['Date & Time', 'Instrument', 'Entry Price', 'Exit Price', 
                            'Stop-loss', 'Take-profit', 'R:R Ratio', 'Result', 'Notes', 'Strategy Name']
        
        # Calculate metrics
        metrics = calculate_performance_metrics(trades_df)
        
        if metrics:
            # Key Metrics Display
            st.subheader("🎯 Key Performance Indicators")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Trades", metrics['total_trades'])
                st.metric("Win Rate", f"{metrics['win_rate']:.1f}%")
            
            with col2:
                st.metric("Winning Trades", metrics['wins'])
                st.metric("Losing Trades", metrics['losses'])
            
            with col3:
                st.metric("Avg R:R Ratio", f"{metrics['avg_rr']:.2f}")
                st.metric("Profit Factor", f"{metrics['profit_factor']:.2f}")
            
            with col4:
                st.metric("Max Win Streak", metrics['max_win_streak'])
                st.metric("Max Loss Streak", metrics['max_loss_streak'])
            
            st.markdown("---")
            
            # Profit/Loss Analysis
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("💰 P&L Analysis")
                st.metric("Total P&L", f"{metrics['total_pnl']:.2f}")
                st.metric("Average Win", f"{metrics['avg_win']:.2f}")
                st.metric("Average Loss", f"{metrics['avg_loss']:.2f}")
                
                # Win/Loss Distribution
                result_counts = trades_df['Result'].value_counts()
                fig_pie = px.pie(
                    values=result_counts.values,
                    names=result_counts.index,
                    title='Win/Loss Distribution',
                    color=result_counts.index,
                    color_discrete_map={'Win': '#00CC96', 'Loss': '#EF553B'}
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                st.subheader("📊 Equity Curve")
                equity_fig = create_equity_curve(trades_df)
                if equity_fig:
                    st.plotly_chart(equity_fig, use_container_width=True)
            
            st.markdown("---")
            
            # Strategy Consistency Score
            st.subheader("🎯 Strategy Consistency Analysis")
            
            consistency = calculate_consistency_score(
                trades_df,
                st.session_state.strategy_data.get('entry_rules', ''),
                st.session_state.strategy_data.get('exit_rules', '')
            )
            
            if consistency:
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    score = consistency['score']
                    st.metric("Consistency Score", f"{score:.0f}/100")
                    st.metric("Rating", consistency['rating'])
                    
                    # Color-coded progress bar
                    if score >= 80:
                        st.success(f"Score: {score:.0f}/100")
                    elif score >= 60:
                        st.info(f"Score: {score:.0f}/100")
                    elif score >= 40:
                        st.warning(f"Score: {score:.0f}/100")
                    else:
                        st.error(f"Score: {score:.0f}/100")
                
                with col2:
                    st.write("**Factors Affecting Consistency:**")
                    if consistency['factors']:
                        for factor in consistency['factors']:
                            st.write(f"• {factor}")
                            
                            # If overtrading detected, show the detailed trade logs
                            if "OVERTRADING" in factor and consistency.get('overtrade_details'):
                                with st.expander("📋 View Overtrading Violations", expanded=True):
                                    st.error("**⚠️ RULE VIOLATION: Maximum 1 trade per day allowed**")
                                    st.write("**Days with multiple trades:**")
                                    for detail in consistency['overtrade_details']:
                                        st.write(f"**📅 {detail['date']}** - **{detail['trade_count']} trades taken:**")
                                        for i, (trade_num, trade_time) in enumerate(zip(detail['trade_numbers'], detail['trade_times']), 1):
                                            st.write(f"   • Trade #{trade_num} at {trade_time}")
                                        st.write("")  # Spacing
                    else:
                        st.write("✅ No major consistency issues detected")
            
            st.markdown("---")
            
            # P&L Analysis Charts
            st.subheader("💰 Detailed P&L Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Daily Net Cumulative P&L
                cumulative_pnl_fig = create_daily_cumulative_pnl_chart(trades_df)
                if cumulative_pnl_fig:
                    st.plotly_chart(cumulative_pnl_fig, use_container_width=True)
            
            with col2:
                # Net Daily P&L
                daily_pnl_fig = create_net_daily_pnl_chart(trades_df)
                if daily_pnl_fig:
                    st.plotly_chart(daily_pnl_fig, use_container_width=True)
            
            st.markdown("---")
            
            # Day of Week Analysis
            st.subheader("📅 Performance by Day of Week")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Trade Distribution by Day
                trade_dist_fig = create_trade_distribution_by_day_chart(trades_df)
                if trade_dist_fig:
                    st.plotly_chart(trade_dist_fig, use_container_width=True)
            
            with col2:
                # Performance by Day
                perf_by_day_fig = create_performance_by_day_chart(trades_df)
                if perf_by_day_fig:
                    st.plotly_chart(perf_by_day_fig, use_container_width=True)

# TAB 4: AI Analysis
with tab4:
    st.header("🤖 AI-Powered Chart Analysis")
    
    if not st.session_state.gemini_api_key:
        st.warning("⚠️ Please enter your Gemini API key in the sidebar to use AI analysis")
    else:
        st.subheader("📸 Upload Trading Chart")
        st.markdown("Upload a screenshot of your trading chart for detailed AI analysis")
        
        uploaded_file = st.file_uploader(
            "Choose a chart image",
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear image of your trading chart with indicators visible"
        )
        
        if uploaded_file is not None:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.image(image, caption="Uploaded Chart", use_container_width=True)
            
            with col2:
                if st.button("🔍 Analyze Chart with Gemini AI", type="primary"):
                    with st.spinner("Analyzing chart... This may take a moment..."):
                        analysis = analyze_chart_with_gemini(image, st.session_state.gemini_api_key)
                        st.session_state.strategy_data['chart_analysis'] = analysis
                        if st.session_state.strategy_data['instrument']:
                            save_strategy_data()
        
        # Display previous analysis if available
        if st.session_state.strategy_data.get('chart_analysis'):
            st.markdown("---")
            st.subheader("📋 AI Analysis Results")
            
            analysis_text = st.session_state.strategy_data['chart_analysis']
            
            # Display in an expandable, formatted container
            with st.container():
                st.markdown(analysis_text)
            
            # Option to clear analysis
            if st.button("🗑️ Clear Analysis"):
                st.session_state.strategy_data['chart_analysis'] = None
                if st.session_state.strategy_data['instrument']:
                    save_strategy_data()
                st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>💡 <strong>Pro Tip:</strong> Consistency and discipline are more important than win rate. 
    A 40% win rate with 2:1 R:R is profitable!</p>
    <p>Track every trade, review regularly, and continuously improve your strategy.</p>
</div>
""", unsafe_allow_html=True)