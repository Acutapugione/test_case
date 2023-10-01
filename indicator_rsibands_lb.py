import talib
import pandas as pd


def rsibands_lb(df, ob_level=70, os_level=30, length=14):
    """
    Calculates the RSIBANDS_LB indicator.

    Args:
        df: DataFrame with price data
        ob_level: Overbought level (default: 70)
        os_level: Oversold level (default: 30)
        length: Period for the RSI calculation (default: 14)

    Returns:
        DataFrame with the following columns:
            * rsi: RSI value
            * ub: Upper band
            * lb: Lower band
            * mid: Midline
    """
    # Calculate the RSI
    rsi = talib.RSI(df["Close"], length)

    # Calculate the upper and lower bands
    ub = rsi + (ob_level - 50) * rsi.diff() / rsi.std()
    lb = rsi - (os_level - 50) * rsi.diff() / rsi.std()

    # Calculate the midline
    mid = (ub + lb) / 2

    # Return the DataFrame with the results
    return pd.DataFrame({
        "rsi": rsi,
        "ub": ub,
        "lb": lb,
        "mid": mid
    })
