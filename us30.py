import csv
import random
from datetime import datetime, timedelta

# ================= CONFIG =================
INSTRUMENT = "US30"
NUM_TRADES = 30
OUTPUT_FILE = "US30_random_trade_logs.csv"

BASE_PRICE = 43000
RISK_PCT = 0.01        # 1% risk
RR_RATIO = 2           # 1:2 fixed

# Random notes pool
NOTES_POOL = [
    "Breakout above resistance with strong volume",
    "EMA trend continuation trade",
    "RSI momentum confirmation",
    "Pullback entry in strong uptrend",
    "Higher high and higher low structure",
    "Fake breakout failed, stop loss hit",
    "Market reversed after entry",
    "Choppy market conditions",
    "Trend exhaustion near resistance",
    "Late entry, momentum faded"
]

# =========================================

trade_logs = []

# Start from a random past date
current_time = datetime.now() - timedelta(days=25)

for i in range(NUM_TRADES):

    # Random gap between trades (30 min to 12 hours)
    gap_minutes = random.randint(30, 720)
    trade_time = current_time + timedelta(minutes=gap_minutes)
    current_time = trade_time

    entry_price = round(BASE_PRICE + random.uniform(-2000, 2000), 2)

    risk_amount = entry_price * RISK_PCT
    stop_loss = round(entry_price - risk_amount, 2)
    take_profit = round(entry_price + (risk_amount * RR_RATIO), 2)

    result = random.choice(["Win", "Loss"])
    exit_price = take_profit if result == "Win" else stop_loss

    notes = random.choice(NOTES_POOL)

    trade_logs.append([
        trade_time.strftime("%Y-%m-%d %H:%M:%S"),
        INSTRUMENT,
        entry_price,
        exit_price,
        stop_loss,
        take_profit,
        result,
        "1:2",
        notes
    ])

# Write CSV
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow([
        "Date & Time",
        "Instrument",
        "Entry Price",
        "Exit Price",
        "Stop-Loss",
        "Take-Profit",
        "Result",
        "R:R",
        "Notes"
    ])
    writer.writerows(trade_logs)

print(f"✅ Random trade log CSV generated: {OUTPUT_FILE}")
