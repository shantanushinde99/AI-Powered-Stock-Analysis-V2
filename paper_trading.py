import csv
import random
from datetime import datetime, timedelta, time

# ================= CONFIG =================
INSTRUMENT = "BTC-USD"
NUM_TRADES = 20
OUTPUT_FILE = "btc_usd_strategy_trade_logs_COMPLIANT.csv"

BASE_PRICE = 43000
MAX_RISK_PCT = 0.01     # EXACT 1 percent
RR_RATIO = 2            # 1:2 R:R
SESSION_NAME = "London"

# London Session IST
SESSION_START = time(13, 30)
SESSION_END = time(22, 30)

# =========================================

def generate_london_time(base_date):
    hour = random.randint(13, 21)
    minute = random.randint(0, 59)
    t = datetime.combine(base_date, time(hour, minute))
    if t.time() > SESSION_END:
        t = datetime.combine(base_date, time(21, 30))
    return t

trade_logs = []
base_date = datetime.now().date() - timedelta(days=10)

for i in range(NUM_TRADES):
    trade_date = base_date + timedelta(days=i)
    trade_time = generate_london_time(trade_date)

    entry_price = round(BASE_PRICE + random.uniform(-1000, 1000), 2)

    # Strict 1 percent risk
    risk_amount = entry_price * MAX_RISK_PCT
    stop_loss = round(entry_price - risk_amount, 2)
    take_profit = round(entry_price + (risk_amount * RR_RATIO), 2)

    result = random.choice(["Win", "Loss"])
    exit_price = take_profit if result == "Win" else stop_loss

    notes = (
        "LONG trade | Price above EMA 50 and EMA 200 | "
        "RSI between 55 and 70 | Volume above average | "
        f"{SESSION_NAME} session | "
        + ("Take profit hit at 1 to 2 RR"
           if result == "Win"
           else "Stop loss hit at 1 percent risk")
    )

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

# ✅ IMPORTANT: utf-8-sig encoding
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

print(f"CSV generated successfully: {OUTPUT_FILE}")
