import pandas as pd
import datetime
import random

def generate_eth_strategy_data(num_records=20):
    symbol = "BINANCE:ETHUSDT"
    qty = 10
    leverage = "10:1"
    data = []
    current_order_id = 3100000000
    base_price = 2500.0
    num_trades = num_records // 2
    start_date = datetime.datetime(2025, 12, 1)
    
    for i in range(num_trades):
        trade_date = start_date + datetime.timedelta(days=i)
        entry_time = trade_date.replace(hour=random.randint(1, 4), 
                                        minute=random.choice([0, 15, 30, 45]), second=0)
        side = random.choice(["Buy", "Sell"])
        exit_side = "Sell" if side == "Buy" else "Buy"
        entry_price = base_price + random.uniform(-50, 50)
        risk = random.uniform(5, 15)
        outcome = random.choice(["Win", "Loss", "BE"])
        
        if outcome == "Win":
            exit_price = entry_price + (2 * risk) if side == "Buy" else entry_price - (2 * risk)
            exit_delay = random.randint(30, 180)
        elif outcome == "Loss":
            exit_price = entry_price - risk if side == "Buy" else entry_price + risk
            exit_delay = random.randint(15, 60)
        else: # Breakeven
            exit_price = entry_price
            exit_delay = random.randint(60, 120)
            
        exit_time = entry_time + datetime.timedelta(minutes=exit_delay)
        
        for p_time, p_side, p_price in [(entry_time, side, entry_price), (exit_time, exit_side, exit_price)]:
            data.append({
                "Symbol": symbol, "Side": p_side, "Type": "Market", "Qty": qty,
                "Limit Price": None, "Stop Price": None, "Fill Price": round(p_price, 2),
                "Status": "Filled", "Commission": None, "Placing Time": p_time.strftime("%Y-%m-%d %H:%M:%S"),
                "Closing Time": p_time.strftime("%Y-%m-%d %H:%M:%S"), "Order ID": current_order_id,
                "Level ID": None, "Leverage": leverage, "Margin": f"{(p_price * qty / 10):,.2f} USD"
            })
            current_order_id += 1
        base_price = entry_price

    return pd.DataFrame(data)

eth_orders = generate_eth_strategy_data(20)
eth_orders.to_csv('ethereum_strategy_order_history.csv', index=False)