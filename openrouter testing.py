import requests

API_KEY = " N2p8UQ5vv3oU8o3OtL8hTOD3JnOTVLSy4TPCMvps"

url = "https://api.marketaux.com/v1/news/all"

params = {
    "api_token": API_KEY,
    "symbols": "AAPL,TSLA",
    "language": "en",
    "limit": 5
}

response = requests.get(url, params=params)
data = response.json()

for article in data.get("data", []):
    print("Title:", article["title"])
    print("Source:", article["source"])
    print("Published:", article["published_at"])
    print("-" * 50)
