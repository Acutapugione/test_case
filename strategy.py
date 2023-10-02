import talib
from helpers import show_progress
from indicator_rsibands import rsibands_lb
import logging


class Strategy:
    """
    A trading strategy that uses the RSIBANDS_LB indicator and the CCI indicator.

    Args:
        df: DataFrame with price data
        ob_level: Overbought level for the RSIBANDS_LB indicator (default: 70)
        os_level: Oversold level for the RSIBANDS_LB indicator (default: 30)
        length: Period for the RSI calculation (default: 14)
    """

    def __init__(self, df, ob_level: int = 70, os_level: int = 30, length: int = 14):
        """
        Initializes the strategy.

        Args:
            df: DataFrame with price data
            ob_level: Overbought level for the RSIBANDS_LB indicator (default: 70)
            os_level: Oversold level for the RSIBANDS_LB indicator (default: 30)
            length: Period for the RSI calculation (default: 14)
        """

        self.df = df.copy()
        self.ob_level = ob_level
        self.os_level = os_level
        self.length = length

    def get_signals(self) -> list[dict]:
        """
        Calculates the trading signals for the strategy.

        Returns:
            A list of dictionaries, each containing the following information about a trading signal:
                * action: True if a trade should be opened, False otherwise
                * entry_price: The price at which to enter the trade
                * tp: The take profit price
                * sl: The stop loss price
        """

        # Calculate the RSIBANDS_LB and CCI indicators
        rsibands_data = rsibands_lb(
            self.df.copy(),
            ob_level=self.ob_level,
            os_level=self.os_level,
            length=self.length,
        )
        cci = talib.CCI(self.df["High"], self.df["Low"], self.df["Close"], 30)

        # Generate the trading signals
        signals = []
        for i in range(len(self.df)):
            prew_price = self.df["Close"].iloc[i-1]
            prew_low = rsibands_data["lb"].iloc[i-1]
            prew_up = rsibands_data["ub"].iloc[i-1]
            curr_price = self.df["Close"].iloc[i]
            curr_low = rsibands_data["lb"].iloc[i]
            curr_up = rsibands_data["ub"].iloc[i]
            # якщо поточна ціна активу перетинає нижню лінію RSIBANDS_LB згори вниз, 
            # а CCI менше “-100”, відкрити LONG
            
            if prew_price > prew_low and curr_price <= curr_low and cci.iloc[i] < -100:
                signal = {
                    "action": "long",
                    "entry_price": self.df["Close"].iloc[i],
                    "tp": self.df["Close"].iloc[i] + self.df["Close"].iloc[i] * 0.01,
                    "sl": self.df["Close"].iloc[i] - self.df["Close"].iloc[i] * 0.004,
                    "position": i,
                }
                signals.append(signal)
                logging.info(f"Generated long signal at {i}")
                logging.info(f"Signal: {signal}")
            #якщо поточна ціна активу перетинає верхню лінію RSIBANDS_LB знизу вгору,
            # а CCI більше “120”, відкрити SHORT
            elif prew_price < prew_up and curr_price >= curr_up and cci.iloc[i] > 120:
                signal = {
                    "action": "short",
                    "entry_price": self.df["Close"].iloc[i],
                    "tp": self.df["Close"].iloc[i] - self.df["Close"].iloc[i] * 0.011,
                    "sl": self.df["Close"].iloc[i] + self.df["Close"].iloc[i] * 0.005,
                    "position": i,
                }
                signals.append(signal)
                logging.info(f"Generated short signal at {i}")
                logging.info(f"Signal: {signal}")
            else:
                signal = {
                    "action": False,
                    "position": None,
                }
                signals.append(signal)
                # logging.info(f"Generated no trading signal at {i}")
            show_progress(i, self.df, "generating the trading signals")
        return signals
