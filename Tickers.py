import pandas as pd
import requests
import io

# NASDAQ official listings (public)
url_nasdaq = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=50000"

headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url_nasdaq, headers=headers).json()

# Convert to DataFrame
df = pd.DataFrame(response["data"]["table"]["rows"])

# Extract required data
df = df[["symbol", "name"]]

# Format: "Company - SYMBOL"
output = [f"{row['name']} - {row['symbol']}" for _, row in df.iterrows()]

print("Total tickers:", len(output))
for item in output:
    print(item)
