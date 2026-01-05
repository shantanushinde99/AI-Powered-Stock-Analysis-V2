# TradeGuide AI - Shared Styles
# Centralized styling for consistent UI across all pages

def get_tradeguide_styles():
    """Returns the shared CSS styles for TradeGuide AI platform"""
    return """
<style>
    /* ========================================
       TRADEGUIDE AI - DESIGN SYSTEM
       ======================================== */
    
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* CSS Variables */
    :root {
        --primary-blue: #0ea5e9;
        --primary-teal: #14b8a6;
        --primary-green: #10b981;
        --text-dark: #1e293b;
        --text-muted: #64748b;
        --text-light: #94a3b8;
        --bg-light: #f8fafc;
        --bg-white: #ffffff;
        --border-color: #e2e8f0;
        --border-hover: #cbd5e1;
        --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.04);
        --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.06);
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 20px;
    }
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .stApp {
        background: var(--bg-light);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Hide Streamlit's auto-generated page list */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* ========================================
       SIDEBAR STYLES
       ======================================== */
    
    [data-testid="stSidebar"] {
        background: var(--bg-white);
        border-right: 1px solid var(--border-color);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0.5rem;
    }
    
    /* Sidebar Logo */
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 1rem 1.25rem 1.25rem;
        border-bottom: 1px solid var(--border-color);
        margin-bottom: 1rem;
    }
    
    .sidebar-logo {
        width: 42px;
        height: 42px;
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-green) 100%);
        border-radius: var(--radius-md);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        color: white;
        flex-shrink: 0;
    }
    
    .sidebar-logo-img {
        width: 42px;
        height: 42px;
        border-radius: var(--radius-md);
        object-fit: contain;
        flex-shrink: 0;
    }
    
    .sidebar-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--text-dark);
        line-height: 1.2;
    }
    
    .sidebar-title span {
        color: var(--primary-blue);
    }
    
    /* Navigation Section */
    .nav-section-label {
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--text-light);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 0.5rem 0;
        margin-top: 0.5rem;
    }
    
    /* ========================================
       PAGE HEADER
       ======================================== */
    
    .page-header {
        margin-bottom: 1.5rem;
    }
    
    .page-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-dark);
        margin-bottom: 0.25rem;
    }
    
    .page-subtitle {
        color: var(--text-muted);
        font-size: 0.95rem;
    }
    
    /* ========================================
       HERO SECTION
       ======================================== */
    
    .hero-card {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-green) 100%);
        border-radius: var(--radius-xl);
        padding: 2.5rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -15%;
        width: 45%;
        height: 200%;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 50%;
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        color: white;
        padding: 0.35rem 0.9rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-bottom: 1rem;
    }
    
    .hero-title {
        font-size: 2rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.75rem;
        line-height: 1.2;
        position: relative;
    }
    
    .hero-text {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.9);
        line-height: 1.6;
        max-width: 550px;
        position: relative;
    }
    
    /* ========================================
       CARDS
       ======================================== */
    
    .card {
        background: var(--bg-white);
        border-radius: var(--radius-lg);
        padding: 1.75rem;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-sm);
        transition: all 0.2s ease;
        margin-bottom: 0.5rem;
    }
    
    .card:hover {
        box-shadow: var(--shadow-md);
    }
    
    .card-icon {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.12) 0%, rgba(16, 185, 129, 0.12) 100%);
        border-radius: var(--radius-md);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .card-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-dark);
        margin-bottom: 0.6rem;
    }
    
    .card-text {
        color: var(--text-muted);
        font-size: 0.95rem;
        line-height: 1.65;
    }
    
    /* Info Card */
    .info-card {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.06) 0%, rgba(16, 185, 129, 0.06) 100%);
        border: 1px solid rgba(14, 165, 233, 0.15);
        border-radius: var(--radius-lg);
        padding: 1.25rem;
        display: flex;
        gap: 1rem;
        align-items: flex-start;
    }
    
    .info-icon {
        font-size: 1.5rem;
        flex-shrink: 0;
    }
    
    .info-title {
        color: var(--primary-blue);
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0 0 0.25rem 0;
    }
    
    .info-text {
        color: var(--text-muted);
        font-size: 0.85rem;
        line-height: 1.5;
        margin: 0;
    }
    
    /* Stat Card */
    .stat-card {
        background: var(--bg-white);
        border-radius: var(--radius-lg);
        padding: 1.25rem;
        border: 1px solid var(--border-color);
        text-align: center;
    }
    
    .stat-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary-blue);
    }
    
    .stat-label {
        color: var(--text-muted);
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    /* ========================================
       SECTION HEADERS
       ======================================== */
    
    .section-header {
        margin-bottom: 1.25rem;
    }
    
    .section-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--text-dark);
        margin-bottom: 0.2rem;
    }
    
    .section-subtitle {
        color: var(--text-muted);
        font-size: 0.9rem;
    }
    
    /* ========================================
       BUTTONS
       ======================================== */
    
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-green) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        padding: 0.6rem 1.25rem !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        transition: all 0.2s ease !important;
        margin-top: 1rem !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.35) !important;
    }
    
    .stButton > button:disabled {
        background: var(--border-color) !important;
        color: var(--text-light) !important;
    }
    
    /* ========================================
       FORM ELEMENTS
       ======================================== */
    
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: var(--radius-sm) !important;
        border-color: var(--border-color) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-blue) !important;
        box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.1) !important;
    }
    
    /* ========================================
       EXPANDERS
       ======================================== */
    
    .streamlit-expanderHeader {
        background: var(--bg-white) !important;
        border-radius: var(--radius-md) !important;
        border: 1px solid var(--border-color) !important;
    }
    
    /* ========================================
       FOOTER
       ======================================== */
    
    .app-footer {
        text-align: center;
        padding: 2rem 0;
        color: var(--text-light);
        font-size: 0.8rem;
        border-top: 1px solid var(--border-color);
        margin-top: 3rem;
    }
    
    .app-footer strong {
        color: var(--text-muted);
    }
    
    /* ========================================
       RESPONSIVE
       ======================================== */
    
    @media (max-width: 768px) {
        .hero-title {
            font-size: 1.5rem;
        }
        
        .hero-card {
            padding: 1.5rem;
        }
        
        .card {
            padding: 1.25rem;
        }
    }
</style>
"""


def get_sidebar_html():
    """Returns the sidebar branding HTML"""
    return """
<div class="sidebar-brand">
    <img src="app/static/logo.png" alt="TradeGuide AI" class="sidebar-logo-img" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
    <div class="sidebar-logo" style="display:none;">📈</div>
    <div class="sidebar-title">Trade<span>Guide</span> AI</div>
</div>
"""


def get_page_header(title: str, subtitle: str = ""):
    """Returns page header HTML"""
    subtitle_html = f'<p class="page-subtitle">{subtitle}</p>' if subtitle else ""
    return f"""
<div class="page-header">
    <h1 class="page-title">{title}</h1>
    {subtitle_html}
</div>
"""


def get_footer_html():
    """Returns footer HTML"""
    return """
<div class="app-footer">
    <p>📈 <strong>TradeGuide AI</strong> — Your intelligent trading companion</p>
    <p>⚠️ For educational purposes only. Not financial advice.</p>
</div>
"""
