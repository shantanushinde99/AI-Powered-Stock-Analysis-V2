import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from utils.styles import get_tradeguide_styles, get_sidebar_html, get_footer_html

# Page Configuration
st.set_page_config(
    page_title="TradeGuide AI - Smart Trading for Beginners",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
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
    st.page_link("Home Page.py", label="🏠  Home", icon=None)
    st.page_link("pages/Trading_Dashboard.py", label="📊  Trading Dashboard")
    st.page_link("pages/Technical_Analysis.py", label="📈  Technical Analysis")
    st.page_link("pages/Strategy_Developer.py", label="🎯  Strategy Developer")
    st.page_link("pages/Investment_Strategist.py", label="💡  Investment Strategist")
    st.page_link("pages/Candle Stick Chart.py", label="🕯️  Candlestick Charts")
    
    st.markdown("---")
    st.markdown('<div class="nav-section-label">Resources</div>', unsafe_allow_html=True)
    st.caption("📚 Trading Guide")
    st.caption("❓ Help Center")

# ============================================
# MAIN CONTENT
# ============================================

# Hero Section
st.markdown("""
<div class="hero-card">
    <span class="hero-badge">🎓 Built for Beginners</span>
    <h1 class="hero-title">Intelligent Guidance for Smarter Trading</h1>
    <p class="hero-text">
        Make informed trading decisions with confidence. TradeGuide AI transforms market data into clear insights, helps you build disciplined strategies, and guides you at every step of your trading journey.
    </p>
</div>
""", unsafe_allow_html=True)

# CTA Buttons
col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
with col1:
    if st.button("🚀 Create Strategy", use_container_width=True):
        st.switch_page("pages/Strategy_Developer.py")
with col2:
    if st.button("📊 Analyze Markets", use_container_width=True):
        st.switch_page("pages/Technical_Analysis.py")
with col3:
    if st.button("📈 View Dashboard", use_container_width=True):
        st.switch_page("pages/Trading_Dashboard.py")

st.markdown("<br>", unsafe_allow_html=True)

# Quick Tip
st.markdown("""
<div class="info-card">
    <div class="info-icon">💡</div>
    <div>
        <p class="info-title">New to Trading?</p>
        <p class="info-text">Start with the <strong>Strategy Developer</strong> — our AI walks you through 
        creating your first trading plan, explaining each concept along the way.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Features Section
st.markdown("""
<div class="section-header">
    <h2 class="section-title">Explore Our Tools</h2>
    <p class="section-subtitle">Everything you need to start your trading journey</p>
</div>
""", unsafe_allow_html=True)

# Feature Cards - Row 1
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🤖</div>
        <h3 class="card-title">AI Trading Dashboard</h3>
        <p class="card-text">Get real-time AI analysis and recommendations with clear explanations for every suggestion.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Dashboard →", key="btn1"):
        st.switch_page("pages/Trading_Dashboard.py")

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🎯</div>
        <h3 class="card-title">Strategy Builder</h3>
        <p class="card-text">Create and test trading strategies step-by-step. No experience needed — AI guides you.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Build Strategy →", key="btn2"):
        st.switch_page("pages/Strategy_Developer.py")

with col3:
    st.markdown("""
    <div class="card">
        <div class="card-icon">📊</div>
        <h3 class="card-title">Technical Analysis</h3>
        <p class="card-text">Visualize market trends with easy-to-understand charts and helpful tooltips.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("View Charts →", key="btn3"):
        st.switch_page("pages/Technical_Analysis.py")

st.markdown("<br>", unsafe_allow_html=True)

# Feature Cards - Row 2
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🕯️</div>
        <h3 class="card-title">Candlestick Patterns</h3>
        <p class="card-text">Learn to read candlestick charts with pattern recognition and educational guides.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Learn Patterns →", key="btn4"):
        st.switch_page("pages/Candle Stick Chart.py")

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-icon">💡</div>
        <h3 class="card-title">Investment Insights</h3>
        <p class="card-text">Get personalized investment advice explained in plain, beginner-friendly language.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Get Insights →", key="btn5"):
        st.switch_page("pages/Investment_Strategist.py")



# Why TradeGuide Section
st.markdown("---")
st.markdown("""
<div class="section-header">
    <h2 class="section-title">Why TradeGuide AI?</h2>
    <p class="section-subtitle">Designed with beginners in mind</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-icon">🎓</div>
        <div class="stat-label">Beginner-First</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-icon">🤖</div>
        <div class="stat-label">AI-Guided</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-icon">📖</div>
        <div class="stat-label">Clear Explanations</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-icon">🛡️</div>
        <div class="stat-label">Risk-Aware</div>
    </div>
    """, unsafe_allow_html=True)

# Learning Section
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div class="section-header">
    <h2 class="section-title">📚 Quick Learning</h2>
    <p class="section-subtitle">Start here if you're new to trading</p>
</div>
""", unsafe_allow_html=True)

with st.expander("What is Trading?"):
    st.markdown("""
    **Trading** is buying and selling financial assets to make a profit.
    - **Buy Low, Sell High** — The basic principle
    - **Market Orders** — Trade at current prices
    - **Stop-Loss** — Automatically limit losses
    """)

with st.expander("How to Read Charts"):
    st.markdown("""
    Charts show price movements over time:
    - 🟢 **Green candles** — Price went up
    - 🔴 **Red candles** — Price went down
    - 📊 **Volume** — Trading activity level
    """)

with st.expander("Creating Your First Strategy"):
    st.markdown("""
    1. **Define goals** — What do you want to achieve?
    2. **Set entry rules** — When to buy?
    3. **Set exit rules** — When to sell?
    4. **Manage risk** — Never risk more than you can afford
    """)

# Footer
st.markdown(get_footer_html(), unsafe_allow_html=True)
