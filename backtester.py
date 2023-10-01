import logging
import numpy as np
import pandas as pd
from helpers import show_progress
from strategy import Strategy


def backtest(df: pd.DataFrame, strategy: Strategy, commission: float = 0.005) -> dict:
    """
    Backtests a trading strategy.

    Args:
        df: DataFrame with price data
        strategy: Strategy object
        commission: Commission per trade (default: 0.005)

    Returns:
        Dict with backtest results:
            * total_profit: Total profit
            * winrate: Win rate
            * profit_factor: Profit factor
    """
    
    # Get the trading signals from the strategy
    signals = strategy.get_signals()

    # Create a list of trades
    trades = []
    i = 0
    for signal in signals:
        i+=1
        if signal["action"]:
            trade = {
                "entry": signal["entry_price"],
                "tp": signal["tp"],
                "sl": signal["sl"],
                "profit": 0,
            }
            trades.append(trade)
            logging.info(f"Added trade to list at index {i}")
            logging.info(f"Trade {trade}")
        
        show_progress(i, signals, 'creating a list of trades')
    # Calculate the profits for each trade
    i = 0
    for trade in trades:
        i += 1
        if trade["tp"] > trade["sl"]:
            trade["profit"] = trade["tp"] - trade["entry"] - trade["sl"] * commission
        else:
            trade["profit"] = -trade["entry"] - trade["sl"] * commission
        logging.info(f"Calculated profit for trade at index {i}")
        logging.info(f"Profit {trade['profit']}")
        show_progress(i, trades, 'calculating the profits')
    # Calculate the total profit, win rate, and profit factor
    total_profit = sum(trade["profit"] for trade in trades)
    winrate = sum(trade["profit"] > 0 for trade in trades) / len(trades)
    profit_factor = np.prod(trade["profit"] + [1])

    logging.info(f"Total profit: {total_profit}")
    logging.info(f"Win rate: {winrate * 100}%")
    logging.info(f"Profit factor: {profit_factor}")
    
    # Return the backtest results
    return {
        "total_profit": total_profit,
        "winrate": f"{winrate * 100}%",
        "profit_factor": profit_factor,
    }
