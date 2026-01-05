import requests
import pandas as pd
from io import StringIO

API_KEY = "M74ZRPOIXNDNY60B"

# -------------------- CRYPTO --------------------
def get_crypto_symbols():
    """
    Alpha Vantage doesn't provide a crypto list API.
    Using a comprehensive list of popular cryptocurrencies.
    """
    cryptos = [
        {"symbol": "BTC", "name": "Bitcoin"},
        {"symbol": "ETH", "name": "Ethereum"},
        {"symbol": "USDT", "name": "Tether"},
        {"symbol": "BNB", "name": "Binance Coin"},
        {"symbol": "USDC", "name": "USD Coin"},
        {"symbol": "XRP", "name": "Ripple"},
        {"symbol": "ADA", "name": "Cardano"},
        {"symbol": "DOGE", "name": "Dogecoin"},
        {"symbol": "SOL", "name": "Solana"},
        {"symbol": "TRX", "name": "TRON"},
        {"symbol": "DOT", "name": "Polkadot"},
        {"symbol": "MATIC", "name": "Polygon"},
        {"symbol": "LTC", "name": "Litecoin"},
        {"symbol": "SHIB", "name": "Shiba Inu"},
        {"symbol": "AVAX", "name": "Avalanche"},
        {"symbol": "DAI", "name": "Dai"},
        {"symbol": "WBTC", "name": "Wrapped Bitcoin"},
        {"symbol": "UNI", "name": "Uniswap"},
        {"symbol": "LINK", "name": "Chainlink"},
        {"symbol": "ATOM", "name": "Cosmos"},
        {"symbol": "XLM", "name": "Stellar"},
        {"symbol": "XMR", "name": "Monero"},
        {"symbol": "BCH", "name": "Bitcoin Cash"},
        {"symbol": "ETC", "name": "Ethereum Classic"},
        {"symbol": "ALGO", "name": "Algorand"},
        {"symbol": "VET", "name": "VeChain"},
        {"symbol": "FIL", "name": "Filecoin"},
        {"symbol": "ICP", "name": "Internet Computer"},
        {"symbol": "APT", "name": "Aptos"},
        {"symbol": "HBAR", "name": "Hedera"},
        {"symbol": "NEAR", "name": "NEAR Protocol"},
        {"symbol": "ARB", "name": "Arbitrum"},
        {"symbol": "OP", "name": "Optimism"},
        {"symbol": "MKR", "name": "Maker"},
        {"symbol": "AAVE", "name": "Aave"},
        {"symbol": "GRT", "name": "The Graph"},
        {"symbol": "SNX", "name": "Synthetix"},
        {"symbol": "CRV", "name": "Curve DAO Token"},
        {"symbol": "SAND", "name": "The Sandbox"},
        {"symbol": "MANA", "name": "Decentraland"},
    ]

    df = pd.DataFrame(cryptos)
    df["type"] = "CRYPTO"
    return df[["type", "symbol", "name"]]


# -------------------- FOREX --------------------
def get_forex_symbols():
    # Alpha Vantage does not expose a forex list,
    # so we generate valid currency pairs
    currencies = [
        "USD", "EUR", "GBP", "INR", "JPY", "AUD",
        "CAD", "CHF", "NZD", "SGD", "HKD"
    ]

    data = []
    for base in currencies:
        for quote in currencies:
            if base != quote:
                data.append({
                    "type": "FOREX",
                    "symbol": f"{base}/{quote}",
                    "name": f"{base} to {quote}"
                })

    return pd.DataFrame(data)


# -------------------- INDIAN STOCKS --------------------
def get_indian_stocks():
    """
    Alpha Vantage does not provide a stock list for India.
    Extended list of popular Indian stocks on BSE and NSE.
    """
    stocks = [
        # Banking & Financial Services
        {"symbol": "RELIANCE.BSE", "name": "Reliance Industries"},
        {"symbol": "TCS.BSE", "name": "Tata Consultancy Services"},
        {"symbol": "INFY.BSE", "name": "Infosys"},
        {"symbol": "HDFCBANK.BSE", "name": "HDFC Bank"},
        {"symbol": "ICICIBANK.BSE", "name": "ICICI Bank"},
        {"symbol": "SBIN.BSE", "name": "State Bank of India"},
        {"symbol": "KOTAKBANK.BSE", "name": "Kotak Mahindra Bank"},
        {"symbol": "AXISBANK.BSE", "name": "Axis Bank"},
        {"symbol": "BAJFINANCE.BSE", "name": "Bajaj Finance"},
        {"symbol": "HDFCLIFE.BSE", "name": "HDFC Life Insurance"},
        {"symbol": "SBILIFE.BSE", "name": "SBI Life Insurance"},
        
        # IT & Technology
        {"symbol": "WIPRO.BSE", "name": "Wipro"},
        {"symbol": "TECHM.BSE", "name": "Tech Mahindra"},
        {"symbol": "HCLTECH.BSE", "name": "HCL Technologies"},
        {"symbol": "LTI.BSE", "name": "LTI Mindtree"},
        
        # Automotive
        {"symbol": "MARUTI.BSE", "name": "Maruti Suzuki"},
        {"symbol": "TATAMOTORS.BSE", "name": "Tata Motors"},
        {"symbol": "M&M.BSE", "name": "Mahindra & Mahindra"},
        {"symbol": "BAJAJ-AUTO.BSE", "name": "Bajaj Auto"},
        {"symbol": "EICHERMOT.BSE", "name": "Eicher Motors"},
        
        # Energy & Power
        {"symbol": "NTPC.BSE", "name": "NTPC"},
        {"symbol": "POWERGRID.BSE", "name": "Power Grid Corporation"},
        {"symbol": "ONGC.BSE", "name": "Oil and Natural Gas Corporation"},
        {"symbol": "BPCL.BSE", "name": "Bharat Petroleum"},
        {"symbol": "IOC.BSE", "name": "Indian Oil Corporation"},
        
        # Pharma & Healthcare
        {"symbol": "SUNPHARMA.BSE", "name": "Sun Pharmaceutical"},
        {"symbol": "DRREDDY.BSE", "name": "Dr. Reddy's Laboratories"},
        {"symbol": "CIPLA.BSE", "name": "Cipla"},
        {"symbol": "DIVISLAB.BSE", "name": "Divi's Laboratories"},
        {"symbol": "APOLLOHOSP.BSE", "name": "Apollo Hospitals"},
        
        # FMCG & Consumer
        {"symbol": "HINDUNILVR.BSE", "name": "Hindustan Unilever"},
        {"symbol": "ITC.BSE", "name": "ITC"},
        {"symbol": "NESTLEIND.BSE", "name": "Nestle India"},
        {"symbol": "BRITANNIA.BSE", "name": "Britannia Industries"},
        {"symbol": "DABUR.BSE", "name": "Dabur India"},
        
        # Metals & Mining
        {"symbol": "TATASTEEL.BSE", "name": "Tata Steel"},
        {"symbol": "HINDALCO.BSE", "name": "Hindalco Industries"},
        {"symbol": "JSWSTEEL.BSE", "name": "JSW Steel"},
        {"symbol": "COALINDIA.BSE", "name": "Coal India"},
        
        # Infrastructure & Construction
        {"symbol": "LT.BSE", "name": "Larsen & Toubro"},
        {"symbol": "ULTRACEMCO.BSE", "name": "UltraTech Cement"},
        {"symbol": "ADANIPORTS.BSE", "name": "Adani Ports"},
        
        # Telecom
        {"symbol": "BHARTIARTL.BSE", "name": "Bharti Airtel"},
        
        # Nifty & Sensex Indices
        {"symbol": "NIFTY50.NSE", "name": "Nifty 50 Index"},
        {"symbol": "SENSEX.BSE", "name": "BSE Sensex Index"},
    ]

    df = pd.DataFrame(stocks)
    df["type"] = "INDIAN_STOCK"
    return df[["type", "symbol", "name"]]


# -------------------- COMBINE ALL --------------------
def fetch_all_alpha_vantage_tickers():
    crypto_df = get_crypto_symbols()
    forex_df = get_forex_symbols()
    india_df = get_indian_stocks()

    return pd.concat([india_df, crypto_df, forex_df], ignore_index=True)


# -------------------- RUN --------------------
if __name__ == "__main__":
    df = fetch_all_alpha_vantage_tickers()

    print(df.head(15))
    print("\nTotal tickers:", len(df))

    df.to_csv("alpha_vantage_combined_tickers.csv", index=False)
