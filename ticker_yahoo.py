import pandas as pd

# -------------------- CRYPTO --------------------
def get_crypto_symbols():
    """
    Yahoo Finance crypto symbols use format: SYMBOL-USD
    Comprehensive list of popular cryptocurrencies.
    """
    cryptos = [
        {"symbol": "BTC-USD", "name": "Bitcoin"},
        {"symbol": "ETH-USD", "name": "Ethereum"},
        {"symbol": "USDT-USD", "name": "Tether"},
        {"symbol": "BNB-USD", "name": "Binance Coin"},
        {"symbol": "USDC-USD", "name": "USD Coin"},
        {"symbol": "XRP-USD", "name": "Ripple"},
        {"symbol": "ADA-USD", "name": "Cardano"},
        {"symbol": "DOGE-USD", "name": "Dogecoin"},
        {"symbol": "SOL-USD", "name": "Solana"},
        {"symbol": "TRX-USD", "name": "TRON"},
        {"symbol": "DOT-USD", "name": "Polkadot"},
        {"symbol": "MATIC-USD", "name": "Polygon"},
        {"symbol": "LTC-USD", "name": "Litecoin"},
        {"symbol": "SHIB-USD", "name": "Shiba Inu"},
        {"symbol": "AVAX-USD", "name": "Avalanche"},
        {"symbol": "DAI-USD", "name": "Dai"},
        {"symbol": "WBTC-USD", "name": "Wrapped Bitcoin"},
        {"symbol": "UNI-USD", "name": "Uniswap"},
        {"symbol": "LINK-USD", "name": "Chainlink"},
        {"symbol": "ATOM-USD", "name": "Cosmos"},
        {"symbol": "XLM-USD", "name": "Stellar"},
        {"symbol": "XMR-USD", "name": "Monero"},
        {"symbol": "BCH-USD", "name": "Bitcoin Cash"},
        {"symbol": "ETC-USD", "name": "Ethereum Classic"},
        {"symbol": "ALGO-USD", "name": "Algorand"},
        {"symbol": "VET-USD", "name": "VeChain"},
        {"symbol": "FIL-USD", "name": "Filecoin"},
        {"symbol": "ICP-USD", "name": "Internet Computer"},
        {"symbol": "APT-USD", "name": "Aptos"},
        {"symbol": "HBAR-USD", "name": "Hedera"},
        {"symbol": "NEAR-USD", "name": "NEAR Protocol"},
        {"symbol": "ARB-USD", "name": "Arbitrum"},
        {"symbol": "OP-USD", "name": "Optimism"},
        {"symbol": "MKR-USD", "name": "Maker"},
        {"symbol": "AAVE-USD", "name": "Aave"},
        {"symbol": "GRT-USD", "name": "The Graph"},
        {"symbol": "SNX-USD", "name": "Synthetix"},
        {"symbol": "CRV-USD", "name": "Curve DAO Token"},
        {"symbol": "SAND-USD", "name": "The Sandbox"},
        {"symbol": "MANA-USD", "name": "Decentraland"},
    ]

    df = pd.DataFrame(cryptos)
    df["type"] = "CRYPTO"
    return df[["type", "symbol", "name"]]


# -------------------- FOREX --------------------
def get_forex_symbols():
    """
    Yahoo Finance forex symbols use specific format:
    - If USD is base: QUOTE=X (e.g., JPY=X for USD/JPY)
    - If USD is quote: BASEUSD=X (e.g., EURUSD=X for EUR/USD)
    - Non-USD pairs: BASEQUOTE=X (e.g., EURGBP=X for EUR/GBP)
    """
    currencies = ["EUR", "GBP", "INR", "JPY", "AUD", "CAD", "CHF", "NZD", "SGD", "HKD", "CNY", "MXN", "BRL"]
    
    data = []
    
    # USD as base currency: USD/XXX = XXX=X
    for quote in currencies:
        data.append({
            "type": "FOREX",
            "symbol": f"{quote}=X",
            "name": f"USD to {quote}"
        })
    
    # USD as quote currency: XXX/USD = XXXUSD=X
    for base in currencies:
        data.append({
            "type": "FOREX",
            "symbol": f"{base}USD=X",
            "name": f"{base} to USD"
        })
    
    # Popular cross pairs (non-USD)
    cross_pairs = [
        {"symbol": "EURGBP=X", "name": "EUR to GBP"},
        {"symbol": "EURJPY=X", "name": "EUR to JPY"},
        {"symbol": "GBPJPY=X", "name": "GBP to JPY"},
        {"symbol": "AUDJPY=X", "name": "AUD to JPY"},
        {"symbol": "EURAUD=X", "name": "EUR to AUD"},
    ]
    data.extend(cross_pairs)

    return pd.DataFrame(data)


# -------------------- INDIAN STOCKS --------------------
def get_indian_stocks():
    """
    Yahoo Finance Indian stock symbols use format:
    - NSE stocks: SYMBOL.NS
    - BSE stocks: SYMBOL.BO
    Extended list of popular Indian stocks.
    """
    stocks = [
        # Banking & Financial Services
        {"symbol": "RELIANCE.NS", "name": "Reliance Industries"},
        {"symbol": "TCS.NS", "name": "Tata Consultancy Services"},
        {"symbol": "INFY.NS", "name": "Infosys"},
        {"symbol": "HDFCBANK.NS", "name": "HDFC Bank"},
        {"symbol": "ICICIBANK.NS", "name": "ICICI Bank"},
        {"symbol": "SBIN.NS", "name": "State Bank of India"},
        {"symbol": "KOTAKBANK.NS", "name": "Kotak Mahindra Bank"},
        {"symbol": "AXISBANK.NS", "name": "Axis Bank"},
        {"symbol": "BAJFINANCE.NS", "name": "Bajaj Finance"},
        {"symbol": "HDFCLIFE.NS", "name": "HDFC Life Insurance"},
        {"symbol": "SBILIFE.NS", "name": "SBI Life Insurance"},
        
        # IT & Technology
        {"symbol": "WIPRO.NS", "name": "Wipro"},
        {"symbol": "TECHM.NS", "name": "Tech Mahindra"},
        {"symbol": "HCLTECH.NS", "name": "HCL Technologies"},
        {"symbol": "LTIM.NS", "name": "LTI Mindtree"},
        
        # Automotive
        {"symbol": "MARUTI.NS", "name": "Maruti Suzuki"},
        {"symbol": "TATAMOTORS.NS", "name": "Tata Motors"},
        {"symbol": "M%26M.NS", "name": "Mahindra & Mahindra"},
        {"symbol": "BAJAJ-AUTO.NS", "name": "Bajaj Auto"},
        {"symbol": "EICHERMOT.NS", "name": "Eicher Motors"},
        
        # Energy & Power
        {"symbol": "NTPC.NS", "name": "NTPC"},
        {"symbol": "POWERGRID.NS", "name": "Power Grid Corporation"},
        {"symbol": "ONGC.NS", "name": "Oil and Natural Gas Corporation"},
        {"symbol": "BPCL.NS", "name": "Bharat Petroleum"},
        {"symbol": "IOC.NS", "name": "Indian Oil Corporation"},
        
        # Pharma & Healthcare
        {"symbol": "SUNPHARMA.NS", "name": "Sun Pharmaceutical"},
        {"symbol": "DRREDDY.NS", "name": "Dr. Reddy's Laboratories"},
        {"symbol": "CIPLA.NS", "name": "Cipla"},
        {"symbol": "DIVISLAB.NS", "name": "Divi's Laboratories"},
        {"symbol": "APOLLOHOSP.NS", "name": "Apollo Hospitals"},
        
        # FMCG & Consumer
        {"symbol": "HINDUNILVR.NS", "name": "Hindustan Unilever"},
        {"symbol": "ITC.NS", "name": "ITC"},
        {"symbol": "NESTLEIND.NS", "name": "Nestle India"},
        {"symbol": "BRITANNIA.NS", "name": "Britannia Industries"},
        {"symbol": "DABUR.NS", "name": "Dabur India"},
        
        # Metals & Mining
        {"symbol": "TATASTEEL.NS", "name": "Tata Steel"},
        {"symbol": "HINDALCO.NS", "name": "Hindalco Industries"},
        {"symbol": "JSWSTEEL.NS", "name": "JSW Steel"},
        {"symbol": "COALINDIA.NS", "name": "Coal India"},
        
        # Infrastructure & Construction
        {"symbol": "LT.NS", "name": "Larsen & Toubro"},
        {"symbol": "ULTRACEMCO.NS", "name": "UltraTech Cement"},
        {"symbol": "ADANIPORTS.NS", "name": "Adani Ports"},
        
        # Telecom
        {"symbol": "BHARTIARTL.NS", "name": "Bharti Airtel"},
        
        # Nifty & Sensex Indices
        {"symbol": "^NSEI", "name": "Nifty 50 Index"},
        {"symbol": "^BSESN", "name": "BSE Sensex Index"},
    ]

    df = pd.DataFrame(stocks)
    df["type"] = "INDIAN_STOCK"
    return df[["type", "symbol", "name"]]


# -------------------- US STOCKS --------------------
def get_us_stocks():
    """
    Yahoo Finance US stock symbols - direct ticker symbols.
    Popular US stocks from various sectors.
    """
    stocks = [
        # Technology
        {"symbol": "AAPL", "name": "Apple Inc."},
        {"symbol": "MSFT", "name": "Microsoft Corporation"},
        {"symbol": "GOOGL", "name": "Alphabet Inc. (Google)"},
        {"symbol": "AMZN", "name": "Amazon.com Inc."},
        {"symbol": "META", "name": "Meta Platforms Inc."},
        {"symbol": "NVDA", "name": "NVIDIA Corporation"},
        {"symbol": "TSLA", "name": "Tesla Inc."},
        {"symbol": "AMD", "name": "Advanced Micro Devices"},
        {"symbol": "INTC", "name": "Intel Corporation"},
        {"symbol": "CRM", "name": "Salesforce Inc."},
        {"symbol": "ORCL", "name": "Oracle Corporation"},
        {"symbol": "ADBE", "name": "Adobe Inc."},
        {"symbol": "NFLX", "name": "Netflix Inc."},
        
        # Financial Services
        {"symbol": "JPM", "name": "JPMorgan Chase & Co."},
        {"symbol": "BAC", "name": "Bank of America Corp."},
        {"symbol": "WFC", "name": "Wells Fargo & Company"},
        {"symbol": "GS", "name": "Goldman Sachs Group"},
        {"symbol": "MS", "name": "Morgan Stanley"},
        {"symbol": "V", "name": "Visa Inc."},
        {"symbol": "MA", "name": "Mastercard Inc."},
        
        # Healthcare
        {"symbol": "JNJ", "name": "Johnson & Johnson"},
        {"symbol": "UNH", "name": "UnitedHealth Group"},
        {"symbol": "PFE", "name": "Pfizer Inc."},
        {"symbol": "ABBV", "name": "AbbVie Inc."},
        {"symbol": "MRK", "name": "Merck & Co. Inc."},
        
        # Consumer
        {"symbol": "WMT", "name": "Walmart Inc."},
        {"symbol": "PG", "name": "Procter & Gamble Co."},
        {"symbol": "KO", "name": "Coca-Cola Company"},
        {"symbol": "PEP", "name": "PepsiCo Inc."},
        {"symbol": "MCD", "name": "McDonald's Corporation"},
        
        # Energy
        {"symbol": "XOM", "name": "Exxon Mobil Corporation"},
        {"symbol": "CVX", "name": "Chevron Corporation"},
        
        # Indices
        {"symbol": "^GSPC", "name": "S&P 500 Index"},
        {"symbol": "^DJI", "name": "Dow Jones Industrial Average"},
        {"symbol": "^IXIC", "name": "NASDAQ Composite Index"},
    ]

    df = pd.DataFrame(stocks)
    df["type"] = "US_STOCK"
    return df[["type", "symbol", "name"]]


# -------------------- COMBINE ALL --------------------
def fetch_all_yahoo_tickers():
    crypto_df = get_crypto_symbols()
    forex_df = get_forex_symbols()
    india_df = get_indian_stocks()
    us_df = get_us_stocks()

    return pd.concat([india_df, us_df, crypto_df, forex_df], ignore_index=True)


# -------------------- RUN --------------------
if __name__ == "__main__":
    df = fetch_all_yahoo_tickers()

    print(df.head(15))
    print("\nTotal tickers:", len(df))

    df.to_csv("yahoo_finance_combined_tickers.csv", index=False)
