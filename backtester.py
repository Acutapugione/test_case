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
    trades = {
        'win': [],
        'loss': [],
    }
    
    i = 0
    current_process = None
    save = None
    for signal in signals:
        i+=1
        if signal["action"]:
            
            # Якщо немає поточної ставки, свторюємо ставку від сигналу
            if not current_process:
                current_process = signal
                save = current_process
                logging.info(f"Open {signal['action']} at index {i}")
            else:
                # Якщо поточна ставка лонг, перевіряємо на StopLoss та TradeProfit
                if current_process['action'] == 'long':
                    # Long
                    if signal['entry_price'] >= current_process['tp'] :
                        # win
                        trades['win'].append({
                            'action': current_process['action'],
                            'start' : current_process['position'],
                            'stop' : signal['position'],
                            'profit_loss':  (current_process['tp'] - current_process['entry_price']) * (1 - commission)**2
                        })
                        current_process = None
                        save['result'] = 'loss'
                    elif signal['entry_price'] <= current_process['sl']:
                        # loss
                        trades['loss'].append({
                            'action': current_process['action'],
                            'start' : current_process['position'],
                            'stop' : signal['position'],
                            'profit_loss':  - (current_process['tp'] - current_process['entry_price']) * (1 - commission)**2
                        })
                        current_process = None
                        save['result'] = 'loss'

                # Якщо поточна ставка Short, перевіряємо на StopLoss та TradeProfit
                elif current_process['action'] == 'short':
                    # Long
                    if signal['entry_price'] <= current_process['tp'] :
                        # win
                        trades['win'].append({
                            'action': current_process['action'],
                            'start' : current_process['position'],
                            'stop' : signal['position'],
                            'profit_loss':  (current_process['tp'] - current_process['entry_price']) * (1 - commission)**2
                        })
                        save['result'] = 'win'
                        current_process = None
                    elif signal['entry_price'] >= current_process['sl']:
                        # loss
                        trades['loss'].append({
                            'action': current_process['action'],
                            'start' : current_process['position'],
                            'stop' : signal['position'],
                            'profit_loss':  - (current_process['tp'] - current_process['entry_price']) * (1 - commission)**2
                        })
                        save['result'] = 'loss'
                        current_process = None
                if current_process == None:
                    logging.info(f"Close {save['action']} at index {i}: {save['result']}")
                    save = None
            # trade = {
            #     "position": signal["position"],
            #     "entry": signal["entry_price"],
            #     "tp": signal["tp"],
            #     "sl": signal["sl"],
            #     "profit": 0,
            # }
            
            
            # trades.append(trade)
            # logging.info(f"Added trade to list at index {i}")
            # logging.info(f"Trade {trade}")
        
        show_progress(i-1, signals, 'creating a list of trades')
    win_total = sum([trade["profit_loss"] for trade in trades['win']]) 
    loss_total = sum([trade["profit_loss"] for trade in trades['loss']])
    total_profit = win_total - loss_total
    winrate = len(trades['win']) / len(trades['win'] + trades['loss'])
    profit_factor = np.prod([trade["profit_loss"] for trade in trades['win'] + trades['loss']])

    logging.info(f"Win total: {win_total}")
    logging.info(f"Loss total: {loss_total}")
    logging.info(f"Total net profit: {total_profit}")
    logging.info(f"Win rate: {winrate * 100}%")
    logging.info(f"Profit factor: {win_total/np.abs(loss_total)}")
    
    # Return the backtest results
    return {
        "total_profit": total_profit,
        "winrate": f"{winrate * 100}%",
        "profit_factor": win_total/loss_total
    }
