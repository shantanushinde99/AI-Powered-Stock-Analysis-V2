import pandas as pd

data = [
    # --- Original 5 trades ---
    {
        "Date & Time": "2025-01-15 10:32",
        "Instrument": "BTC-USD",
        "Entry Price": 89200,
        "Exit Price": 89767,
        "Stop-Loss": 88500,
        "Take-Profit": 90500,
        "Result": "Win",
        "R:R": 1.8,
        "Notes": "Breakout trade above resistance"
    },
    {
        "Date & Time": "2025-01-16 14:10",
        "Instrument": "BTC-USD",
        "Entry Price": 89850,
        "Exit Price": 89500,
        "Stop-Loss": 89200,
        "Take-Profit": 91000,
        "Result": "Loss",
        "R:R": 0.7,
        "Notes": "False breakout, volume weak"
    },
    {
        "Date & Time": "2025-01-17 09:50",
        "Instrument": "BTC-USD",
        "Entry Price": 88700,
        "Exit Price": 89767,
        "Stop-Loss": 88000,
        "Take-Profit": 90000,
        "Result": "Win",
        "R:R": 1.4,
        "Notes": "Trend continuation trade"
    },
    {
        "Date & Time": "2025-01-18 12:20",
        "Instrument": "BTC-USD",
        "Entry Price": 90300,
        "Exit Price": 89767,
        "Stop-Loss": 89500,
        "Take-Profit": 91500,
        "Result": "Loss",
        "R:R": 1.0,
        "Notes": "Entered late, retracement happened"
    },
    {
        "Date & Time": "2025-01-19 18:05",
        "Instrument": "BTC-USD",
        "Entry Price": 89050,
        "Exit Price": 89767,
        "Stop-Loss": 88300,
        "Take-Profit": 90500,
        "Result": "Win",
        "R:R": 1.2,
        "Notes": "EMA bounce entry"
    },

    # --- 30 New Trades ---
    {
        "Date & Time": "2025-01-20 11:15",
        "Instrument": "BTC-USD",
        "Entry Price": 89500,
        "Exit Price": 90120,
        "Stop-Loss": 88800,
        "Take-Profit": 90500,
        "Result": "Win",
        "R:R": 1.5,
        "Notes": "Support bounce"
    },
    {
        "Date & Time": "2025-01-21 09:40",
        "Instrument": "BTC-USD",
        "Entry Price": 90250,
        "Exit Price": 89600,
        "Stop-Loss": 89700,
        "Take-Profit": 91500,
        "Result": "Loss",
        "R:R": 0.8,
        "Notes": "Failed continuation setup"
    },
    {
        "Date & Time": "2025-01-22 15:05",
        "Instrument": "BTC-USD",
        "Entry Price": 88900,
        "Exit Price": 89980,
        "Stop-Loss": 88250,
        "Take-Profit": 90500,
        "Result": "Win",
        "R:R": 1.6,
        "Notes": "Bullish divergence"
    },
    {
        "Date & Time": "2025-01-23 13:10",
        "Instrument": "BTC-USD",
        "Entry Price": 90500,
        "Exit Price": 90030,
        "Stop-Loss": 89750,
        "Take-Profit": 91800,
        "Result": "Loss",
        "R:R": 1.0,
        "Notes": "News volatility hit stop"
    },
    {
        "Date & Time": "2025-01-24 16:45",
        "Instrument": "BTC-USD",
        "Entry Price": 89250,
        "Exit Price": 90110,
        "Stop-Loss": 88500,
        "Take-Profit": 90500,
        "Result": "Win",
        "R:R": 1.3,
        "Notes": "Strong buying zone"
    },
    {
        "Date & Time": "2025-01-25 10:20",
        "Instrument": "BTC-USD",
        "Entry Price": 89800,
        "Exit Price": 89300,
        "Stop-Loss": 89050,
        "Take-Profit": 91000,
        "Result": "Loss",
        "R:R": 0.9,
        "Notes": "Breakout failed"
    },
    {
        "Date & Time": "2025-01-26 17:55",
        "Instrument": "BTC-USD",
        "Entry Price": 88450,
        "Exit Price": 89570,
        "Stop-Loss": 87900,
        "Take-Profit": 90000,
        "Result": "Win",
        "R:R": 1.7,
        "Notes": "Oversold bounce"
    },
    {
        "Date & Time": "2025-01-27 14:32",
        "Instrument": "BTC-USD",
        "Entry Price": 90320,
        "Exit Price": 89780,
        "Stop-Loss": 89500,
        "Take-Profit": 91500,
        "Result": "Loss",
        "R:R": 1.1,
        "Notes": "Premature long entry"
    },
    {
        "Date & Time": "2025-01-28 11:14",
        "Instrument": "BTC-USD",
        "Entry Price": 88880,
        "Exit Price": 89810,
        "Stop-Loss": 88150,
        "Take-Profit": 90300,
        "Result": "Win",
        "R:R": 1.4,
        "Notes": "Perfect trend continuation"
    },
    {
        "Date & Time": "2025-01-29 18:40",
        "Instrument": "BTC-USD",
        "Entry Price": 90150,
        "Exit Price": 89700,
        "Stop-Loss": 89500,
        "Take-Profit": 91000,
        "Result": "Loss",
        "R:R": 0.7,
        "Notes": "Low volume pullback"
    },

    # more data
    {
        "Date & Time": "2025-01-30 09:50",
        "Instrument": "BTC-USD",
        "Entry Price": 89050,
        "Exit Price": 89930,
        "Stop-Loss": 88300,
        "Take-Profit": 90500,
        "Result": "Win",
        "R:R": 1.5,
        "Notes": "EMA support bounce"
    },
    {
        "Date & Time": "2025-01-31 13:22",
        "Instrument": "BTC-USD",
        "Entry Price": 89500,
        "Exit Price": 88910,
        "Stop-Loss": 88800,
        "Take-Profit": 91000,
        "Result": "Loss",
        "R:R": 0.6,
        "Notes": "Reversal misread"
    },
    {
        "Date & Time": "2025-02-01 16:05",
        "Instrument": "BTC-USD",
        "Entry Price": 88200,
        "Exit Price": 89770,
        "Stop-Loss": 87500,
        "Take-Profit": 90000,
        "Result": "Win",
        "R:R": 2.0,
        "Notes": "High-conviction dip buy"
    },
    {
        "Date & Time": "2025-02-02 11:40",
        "Instrument": "BTC-USD",
        "Entry Price": 90500,
        "Exit Price": 89960,
        "Stop-Loss": 89500,
        "Take-Profit": 92000,
        "Result": "Loss",
        "R:R": 0.9,
        "Notes": "Price rejected at resistance"
    },
    {
        "Date & Time": "2025-02-03 10:31",
        "Instrument": "BTC-USD",
        "Entry Price": 88900,
        "Exit Price": 90210,
        "Stop-Loss": 88200,
        "Take-Profit": 90500,
        "Result": "Win",
        "R:R": 1.8,
        "Notes": "Bullish structure intact"
    },
    {
        "Date & Time": "2025-02-04 17:20",
        "Instrument": "BTC-USD",
        "Entry Price": 89750,
        "Exit Price": 89320,
        "Stop-Loss": 89000,
        "Take-Profit": 91000,
        "Result": "Loss",
        "R:R": 0.85,
        "Notes": "Choppy market"
    },
    {
        "Date & Time": "2025-02-05 12:15",
        "Instrument": "BTC-USD",
        "Entry Price": 88350,
        "Exit Price": 89580,
        "Stop-Loss": 87700,
        "Take-Profit": 90000,
        "Result": "Win",
        "R:R": 1.9,
        "Notes": "RSI oversold + trendline bounce"
    },
    {
        "Date & Time": "2025-02-06 14:40",
        "Instrument": "BTC-USD",
        "Entry Price": 90100,
        "Exit Price": 89800,
        "Stop-Loss": 89400,
        "Take-Profit": 91500,
        "Result": "Loss",
        "R:R": 0.8,
        "Notes": "No follow-through"
    },
    {
        "Date & Time": "2025-02-07 09:55",
        "Instrument": "BTC-USD",
        "Entry Price": 89020,
        "Exit Price": 90330,
        "Stop-Loss": 88300,
        "Take-Profit": 90500,
        "Result": "Win",
        "R:R": 1.6,
        "Notes": "Strong bullish candle"
    },
    {
        "Date & Time": "2025-02-08 18:22",
        "Instrument": "BTC-USD",
        "Entry Price": 89300,
        "Exit Price": 88840,
        "Stop-Loss": 88700,
        "Take-Profit": 91000,
        "Result": "Loss",
        "R:R": 0.7,
        "Notes": "Fakeout wick"
    },

    # Adds even more
    {
        "Date & Time": "2025-02-09 11:30",
        "Instrument": "BTC-USD",
        "Entry Price": 88150,
        "Exit Price": 89500,
        "Stop-Loss": 87500,
        "Take-Profit": 90000,
        "Result": "Win",
        "R:R": 1.9,
        "Notes": "Market flushed then recovered"
    },
    {
        "Date & Time": "2025-02-10 15:15",
        "Instrument": "BTC-USD",
        "Entry Price": 89750,
        "Exit Price": 89040,
        "Stop-Loss": 88700,
        "Take-Profit": 91000,
        "Result": "Loss",
        "R:R": 0.7,
        "Notes": "Breakout trap"
    },
    {
        "Date & Time": "2025-02-11 10:45",
        "Instrument": "BTC-USD",
        "Entry Price": 88900,
        "Exit Price": 89970,
        "Stop-Loss": 88250,
        "Take-Profit": 90500,
        "Result": "Win",
        "R:R": 1.5,
        "Notes": "High volume breakout"
    },
    {
        "Date & Time": "2025-02-12 13:55",
        "Instrument": "BTC-USD",
        "Entry Price": 90150,
        "Exit Price": 89580,
        "Stop-Loss": 89400,
        "Take-Profit": 91500,
        "Result": "Loss",
        "R:R": 0.9,
        "Notes": "Bad timing"
    },
    {
        "Date & Time": "2025-02-13 09:20",
        "Instrument": "BTC-USD",
        "Entry Price": 88320,
        "Exit Price": 89670,
        "Stop-Loss": 87650,
        "Take-Profit": 90000,
        "Result": "Win",
        "R:R": 1.8,
        "Notes": "Strong trend day"
    }
]

# Create DataFrame
df = pd.DataFrame(data)

# Save file
file_path = r"D:\AI-Powered-Stock-Analysis-and-CandleStick-Chart-main\AI-Powered-Stock-Analysis-and-CandleStick-Chart-main\Trade_logs.csv"
df.to_csv(file_path, index=False)

# Verify by loading the file
loaded_df = pd.read_csv(file_path)

print("File saved to:", file_path)
print("\nLoaded DataFrame:")
print(loaded_df)
