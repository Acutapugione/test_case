import talib
from helpers import show_progress
from indicator_rsibands_lb import rsibands_lb
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
            if (
                rsibands_data["ub"].iloc[i] < self.df["Close"].iloc[i]
                and cci.iloc[i] < -100
            ):
                signal = {
                    "action": True,
                    "entry_price": self.df["Close"].iloc[i],
                    "tp": self.df["Close"].iloc[i] * 1.01,
                    "sl": self.df["Close"].iloc[i] * 1.004,
                    "position": "long",
                }
                signals.append(signal)
                logging.info(f"Generated long signal at {i}")
                logging.info(f"Signal: {signal}")
            elif (
                rsibands_data["lb"].iloc[i] > self.df["Close"].iloc[i]
                and cci.iloc[i] > 120
            ):
                signal = {
                    "action": True,
                    "entry_price": self.df["Close"].iloc[i],
                    "tp": self.df["Close"].iloc[i] * 1.11,
                    "sl": self.df["Close"].iloc[i] * 1.05,
                    "position": "short",
                }
                signals.append(signal)
                logging.info(f"Generated short signal at {i}")
                logging.info(f"Signal: {signal}")
            else:
                signal = {
                    "action": False,
                    "entry_price": self.df["Close"].iloc[i],
                    "tp": self.df["Close"].iloc[i],
                    "sl": self.df["Close"].iloc[i],
                    "position": None,
                }
                signals.append(signal)
                logging.info(f"Generated no trading signal at {i}")
            show_progress(i, self.df, "generating the trading signals")
        return signals
