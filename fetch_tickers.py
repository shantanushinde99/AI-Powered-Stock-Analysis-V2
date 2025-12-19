"""
Asset Ticker Fetcher using Yahoo Finance
This program fetches stock, crypto, and forex ticker symbols.
"""

import requests
import json
import csv
import os
from datetime import datetime
import yfinance as yf

class AssetTickerFetcher:
    def __init__(self):
        """
        Initialize the Asset Ticker Fetcher
        Uses Yahoo Finance for ticker data
        """
        pass
    
    def fetch_stock_symbols(self, exchange='US'):
        """
        Fetch stock symbols using Yahoo Finance
        
        Args:
            exchange (str): Exchange code (e.g., 'US', 'TO', 'L', 'HK')
        
        Returns:
            list: List of dictionaries containing stock information
        """
        print(f"Fetching stock symbols for {exchange} market...")
        
        # Note: Yahoo Finance doesn't provide a comprehensive ticker list API
        # This is a placeholder - you may want to use a CSV file with tickers
        # or another data source
        
        print("Warning: This fetcher now uses Yahoo Finance which doesn't provide a ticker list API.")
        print("Consider using a pre-defined list of tickers or alternative data source.")
        
        try:
            # Return empty list as Yahoo Finance doesn't provide this functionality
            return []
            response.raise_for_status()
            data = response.json()
            
            # Format the data
            stocks = []
            for item in data:
                stocks.append({
                    'symbol': item.get('symbol', 'N/A'),
                    'description': item.get('description', 'N/A'),
                    'displaySymbol': item.get('displaySymbol', 'N/A'),
                    'type': item.get('type', 'N/A'),
                    'exchange': exchange
                })
            
            print(f"Successfully fetched {len(stocks)} stock symbols")
            return stocks
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching stock data: {e}")
            return []
    
    def fetch_all_exchanges(self):
        """
        Fetch list of supported exchanges from Finnhub
        
        Returns:
            list: List of exchange codes
        """
        if not self.finnhub_key:
            print("Error: Finnhub API key is required")
            return []
        
        url = f"{self.finnhub_base_url}/stock/exchange"
        params = {'token': self.finnhub_key}
        
        print("Fetching available exchanges...")
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            exchanges = response.json()
            
            print(f"Found {len(exchanges)} exchanges")
            return exchanges
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching exchanges: {e}")
            return []
    
    def fetch_crypto_currencies(self):
        """
        Fetch list of all cryptocurrencies using Finnhub API
        
        Returns:
            list: List of dictionaries containing crypto currency information
        """
        if not self.finnhub_key:
            print("Error: Finnhub API key is required for crypto data")
            return []
        
        url = f"{self.finnhub_base_url}/crypto/symbol"
        params = {
            'exchange': 'binance',  # Using Binance as default exchange
            'token': self.finnhub_key
        }
        
        print("Fetching cryptocurrency list from Finnhub...")
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Format the data
            cryptos = []
            for item in data:
                cryptos.append({
                    'symbol': item.get('symbol', 'N/A'),
                    'description': item.get('description', 'N/A'),
                    'displaySymbol': item.get('displaySymbol', 'N/A')
                })
            
            print(f"Successfully fetched {len(cryptos)} cryptocurrencies")
            return cryptos
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching crypto data: {e}")
            return []
    
    def fetch_forex_pairs(self):
        """
        Fetch forex currency pairs using FCS API
        
        Returns:
            list: List of dictionaries containing forex pair information
        """
        if not self.fcs_key:
            print("Error: FCS API key is required for forex data")
            return []
        
        url = f"{self.fcs_base_url}/forex/list"
        params = {'access_key': self.fcs_key}
        
        print("Fetching forex pairs from FCS API...")
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') and data.get('response'):
                forex_pairs = []
                for item in data['response']:
                    forex_pairs.append({
                        'symbol': item.get('symbol', 'N/A'),
                        'name': item.get('name', 'N/A'),
                        'category': item.get('category', 'N/A'),
                        'decimals': item.get('decimals', 'N/A')
                    })
                
                print(f"Successfully fetched {len(forex_pairs)} forex pairs")
                return forex_pairs
            else:
                print("No forex data received from API")
                return []
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching forex data: {e}")
            return []
    
    def fetch_forex_symbols(self, exchange='oanda'):
        """
        Fetch forex symbols using Finnhub API
        
        Args:
            exchange (str): Forex exchange (e.g., 'oanda', 'fxcm', 'ic markets')
        
        Returns:
            list: List of dictionaries containing forex symbol information
        """
        if not self.finnhub_key:
            print("Error: Finnhub API key is required for forex data")
            return []
        
        url = f"{self.finnhub_base_url}/forex/symbol"
        params = {
            'exchange': exchange,
            'token': self.finnhub_key
        }
        
        print(f"Fetching forex symbols from Finnhub (Exchange: {exchange})...")
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Format the data
            forex_symbols = []
            for item in data:
                forex_symbols.append({
                    'symbol': item.get('symbol', 'N/A'),
                    'description': item.get('description', 'N/A'),
                    'displaySymbol': item.get('displaySymbol', 'N/A')
                })
            
            print(f"Successfully fetched {len(forex_symbols)} forex symbols")
            return forex_symbols
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching forex symbols: {e}")
            return []
    
    def search_ticker(self, keywords):
        """
        Search for tickers by keywords using Finnhub API
        
        Args:
            keywords (str): Search keywords
        
        Returns:
            list: List of matching tickers
        """
        if not self.finnhub_key:
            print("Error: Finnhub API key is required for search")
            return []
        
        url = f"{self.finnhub_base_url}/search"
        params = {
            'q': keywords,
            'token': self.finnhub_key
        }
        
        print(f"Searching for tickers matching '{keywords}'...")
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            matches = data.get('result', [])
            print(f"Found {len(matches)} matches")
            return matches
            
        except requests.exceptions.RequestException as e:
            print(f"Error searching tickers: {e}")
            return []
    
    def save_to_csv(self, tickers, filename='tickers.csv'):
        """
        Save ticker data to CSV file
        
        Args:
            tickers (list): List of ticker dictionaries
            filename (str): Output filename
        """
        if not tickers:
            print("No tickers to save")
            return
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=tickers[0].keys())
                writer.writeheader()
                writer.writerows(tickers)
            
            print(f"Saved {len(tickers)} tickers to {filename}")
            
        except Exception as e:
            print(f"Error saving to CSV: {e}")
    
    def save_to_json(self, tickers, filename='tickers.json'):
        """
        Save ticker data to JSON file
        
        Args:
            tickers (list): List of ticker dictionaries
            filename (str): Output filename
        """
        if not tickers:
            print("No tickers to save")
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(tickers, f, indent=2)
            
            print(f"Saved {len(tickers)} tickers to {filename}")
            
        except Exception as e:
            print(f"Error saving to JSON: {e}")
    
    def display_tickers(self, tickers, limit=20, ticker_type='stock'):
        """
        Display tickers in a formatted way
        
        Args:
            tickers (list): List of ticker dictionaries
            limit (int): Number of tickers to display
            ticker_type (str): Type of ticker ('stock', 'crypto', 'forex', 'currency')
        """
        if not tickers:
            print("No tickers to display")
            return
        
        if ticker_type == 'stock':
            print(f"\n{'Symbol':<20} {'Description':<50} {'Exchange':<10}")
            print("-" * 80)
            
            for i, ticker in enumerate(tickers[:limit]):
                symbol = ticker.get('symbol', 'N/A')
                description = ticker.get('description', 'N/A')[:47] + '...' if len(ticker.get('description', 'N/A')) > 50 else ticker.get('description', 'N/A')
                exchange = ticker.get('exchange', 'N/A')
                
                print(f"{symbol:<20} {description:<50} {exchange:<10}")
        
        elif ticker_type == 'crypto':
            print(f"\n{'Symbol':<20} {'Description':<60}")
            print("-" * 80)
            
            for i, ticker in enumerate(tickers[:limit]):
                symbol = ticker.get('symbol', 'N/A')
                description = ticker.get('description', 'N/A')[:57] + '...' if len(ticker.get('description', 'N/A')) > 60 else ticker.get('description', 'N/A')
                
                print(f"{symbol:<20} {description:<60}")
        
        elif ticker_type == 'forex':
            print(f"\n{'Symbol':<20} {'Name':<40} {'Category':<20}")
            print("-" * 80)
            
            for i, ticker in enumerate(tickers[:limit]):
                symbol = ticker.get('symbol', 'N/A')
                name = ticker.get('name', ticker.get('description', 'N/A'))[:37] + '...' if len(ticker.get('name', ticker.get('description', 'N/A'))) > 40 else ticker.get('name', ticker.get('description', 'N/A'))
                category = ticker.get('category', 'N/A')
                
                print(f"{symbol:<20} {name:<40} {category:<20}")
        
        elif ticker_type == 'forex_symbol':
            print(f"\n{'Symbol':<20} {'Description':<60}")
            print("-" * 80)
            
            for i, ticker in enumerate(tickers[:limit]):
                symbol = ticker.get('symbol', 'N/A')
                description = ticker.get('description', 'N/A')[:57] + '...' if len(ticker.get('description', 'N/A')) > 60 else ticker.get('description', 'N/A')
                
                print(f"{symbol:<20} {description:<60}")
        
        if len(tickers) > limit:
            print(f"\n... and {len(tickers) - limit} more")
        print(f"\nTotal: {len(tickers)} items")


def main():
    """Main function to run the asset ticker fetcher"""
    
    # Get API keys from environment variables or user input
    finnhub_key = os.getenv('FINNHUB_API_KEY')
    fcs_key = os.getenv('FCS_API_KEY')
    
    if not finnhub_key:
        print("Finnhub API Key not found in environment variables.")
        finnhub_key = input("Please enter your Finnhub API key (or press Enter to skip): ").strip()
    
    if not fcs_key:
        print("FCS API Key not found in environment variables.")
        fcs_key = input("Please enter your FCS API key (or press Enter to skip): ").strip()
    
    if not finnhub_key and not fcs_key:
        print("Error: At least one API key is required!")
        print("Get free API keys from:")
        print("  - Finnhub: https://finnhub.io/register")
        print("  - FCS: https://fcsapi.com/")
        return
    
    # Create fetcher instance
    fetcher = AssetTickerFetcher(finnhub_key=finnhub_key, fcs_key=fcs_key)
    
    # Menu
    while True:
        print("\n" + "="*80)
        print("Asset Ticker Fetcher - Finnhub & FCS APIs")
        print("="*80)
        print("STOCKS (Finnhub):")
        print("  1. Fetch US stock symbols")
        print("  2. Fetch stock symbols from other exchanges")
        print("  3. List available exchanges")
        print("\nCRYPTOCURRENCIES (Finnhub):")
        print("  4. Fetch all cryptocurrencies")
        print("\nFOREX:")
        print("  5. Fetch forex pairs (FCS API)")
        print("  6. Fetch forex symbols (Finnhub)")
        print("\nSEARCH (Finnhub):")
        print("  7. Search for specific ticker")
        print("\n  8. Exit")
        print("="*80)
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            stocks = fetcher.fetch_stock_symbols('US')
            if stocks:
                fetcher.display_tickers(stocks, limit=20, ticker_type='stock')
                
                save = input("\nDo you want to save the data? (csv/json/no): ").strip().lower()
                if save == 'csv':
                    filename = f"us_stocks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                    fetcher.save_to_csv(stocks, filename)
                elif save == 'json':
                    filename = f"us_stocks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    fetcher.save_to_json(stocks, filename)
        
        elif choice == '2':
            exchange = input("Enter exchange code (e.g., 'TO' for Toronto, 'L' for London, 'HK' for Hong Kong): ").strip().upper()
            if exchange:
                stocks = fetcher.fetch_stock_symbols(exchange)
                if stocks:
                    fetcher.display_tickers(stocks, limit=20, ticker_type='stock')
                    
                    save = input("\nDo you want to save the data? (csv/json/no): ").strip().lower()
                    if save == 'csv':
                        filename = f"{exchange}_stocks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                        fetcher.save_to_csv(stocks, filename)
                    elif save == 'json':
                        filename = f"{exchange}_stocks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                        fetcher.save_to_json(stocks, filename)
        
        elif choice == '3':
            exchanges = fetcher.fetch_all_exchanges()
            if exchanges:
                print("\nAvailable Exchanges:")
                print("-" * 40)
                for ex in exchanges:
                    print(f"  {ex}")
        
        elif choice == '4':
            cryptos = fetcher.fetch_crypto_currencies()
            if cryptos:
                fetcher.display_tickers(cryptos, limit=20, ticker_type='crypto')
                
                save = input("\nDo you want to save the data? (csv/json/no): ").strip().lower()
                if save == 'csv':
                    filename = f"cryptocurrencies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                    fetcher.save_to_csv(cryptos, filename)
                elif save == 'json':
                    filename = f"cryptocurrencies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    fetcher.save_to_json(cryptos, filename)
        
        elif choice == '5':
            forex_pairs = fetcher.fetch_forex_pairs()
            if forex_pairs:
                fetcher.display_tickers(forex_pairs, limit=20, ticker_type='forex')
                
                save = input("\nDo you want to save the data? (csv/json/no): ").strip().lower()
                if save == 'csv':
                    filename = f"forex_pairs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                    fetcher.save_to_csv(forex_pairs, filename)
                elif save == 'json':
                    filename = f"forex_pairs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    fetcher.save_to_json(forex_pairs, filename)
        
        elif choice == '6':
            exchange = input("Enter forex exchange (default: 'oanda', options: 'fxcm', 'ic markets'): ").strip().lower() or 'oanda'
            forex_symbols = fetcher.fetch_forex_symbols(exchange)
            if forex_symbols:
                fetcher.display_tickers(forex_symbols, limit=20, ticker_type='forex_symbol')
                
                save = input("\nDo you want to save the data? (csv/json/no): ").strip().lower()
                if save == 'csv':
                    filename = f"forex_symbols_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                    fetcher.save_to_csv(forex_symbols, filename)
                elif save == 'json':
                    filename = f"forex_symbols_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    fetcher.save_to_json(forex_symbols, filename)
        
        elif choice == '7':
            keywords = input("Enter search keywords (e.g., 'Apple', 'AAPL', 'Bitcoin'): ").strip()
            if keywords:
                matches = fetcher.search_ticker(keywords)
                if matches:
                    print(f"\n{'Symbol':<20} {'Description':<40} {'Type':<15}")
                    print("-" * 75)
                    for match in matches:
                        symbol = match.get('symbol', 'N/A')
                        description = match.get('description', 'N/A')[:37] + '...' if len(match.get('description', 'N/A')) > 40 else match.get('description', 'N/A')
                        ticker_type = match.get('type', 'N/A')
                        print(f"{symbol:<20} {description:<40} {ticker_type:<15}")
        
        elif choice == '8':
            print("\nThank you for using Asset Ticker Fetcher!")
            break
        
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()