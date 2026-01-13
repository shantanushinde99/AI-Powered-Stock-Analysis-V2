import csv
import random
from datetime import datetime, timedelta

# ================= CONFIG =================
INSTRUMENT = "BTC-USD"
NUM_TRADES = 100
OUTPUT_FILE = "btc_usd_strategy_trade_logs_OVERTRADING_TEST.csv"

BASE_PRICE = 43000
MAX_RISK_PCT = 0.01
RR_RATIO = 2

MIN_GAP_MINUTES = 60     # minimum 1 hour between trades
MAX_GAP_MINUTES = 360    # maximum 6 hours
MAX_TRADES_PER_DAY = 3

# =========================================

trade_logs = []

start_date = datetime.now().date() - timedelta(days=20)
trade_count = 0
current_date = start_date

while trade_count < NUM_TRADES:

    # Decide how many trades today (1–3)
    trades_today = random.randint(1, MAX_TRADES_PER_DAY)

    # Start time anywhere in the day
    last_trade_time = datetime.combine(
        current_date,
        datetime.min.time()
    ) + timedelta(minutes=random.randint(0, 600))

    for _ in range(trades_today):
        if trade_count >= NUM_TRADES:
            break

        # Enforce realistic gap
        gap_minutes = random.randint(MIN_GAP_MINUTES, MAX_GAP_MINUTES)
        trade_time = last_trade_time + timedelta(minutes=gap_minutes)

        last_trade_time = trade_time

        entry_price = round(BASE_PRICE + random.uniform(-1000, 1000), 2)

        risk_amount = entry_price * MAX_RISK_PCT
        stop_loss = round(entry_price - risk_amount, 2)
        take_profit = round(entry_price + (risk_amount * RR_RATIO), 2)

        result = random.choice(["Win", "Loss"])
        exit_price = take_profit if result == "Win" else stop_loss

        notes = (
            "LONG trade | EMA 50 above EMA 200 | "
            "RSI 55-70 | Volume above average | "
            "Risk 1 percent | "
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

        trade_count += 1

    # Move to next day
    current_date += timedelta(days=1)

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

print("CSV generated for SAME-DAY over-trading analysis.")
