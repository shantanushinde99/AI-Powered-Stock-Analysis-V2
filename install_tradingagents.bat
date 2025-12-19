@echo off
echo ============================================
echo TradingAgents Framework - Installation
echo ============================================
echo.

echo [1/3] Installing main dependencies...
pip install -r requirements.txt

echo.
echo [2/3] Installing TradingAgents dependencies...
cd TradingAgents
pip install -r requirements.txt
cd ..

echo.
echo [3/3] Creating .env file if not exists...
if not exist .env (
    copy .env.example .env
    echo .env file created! Please edit it with your API keys.
) else (
    echo .env file already exists.
)

echo.
echo ============================================
echo Installation Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Edit .env file and add your API keys
echo 2. Run: streamlit run "Home Page.py"
echo.
echo See TRADINGAGENTS_SETUP.md for detailed guide.
echo.
pause
