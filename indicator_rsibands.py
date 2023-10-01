import talib
import pandas as pd


def rsibands_lb(df, ob_level=70, os_level=30, length=14, src="Close"):
    """
    Calculates the RSIBANDS_LB indicator using PineScript logic.

    Args:
        df: DataFrame with price data
        ob_level: Overbought level (default: 70)
        os_level: Oversold level (default: 30)
        length: Period for the RSI calculation (default: 14)
        src: Source price column (default: "Close")

    Returns:
        DataFrame with the following columns:
            * rsi: RSI value
            * ub: Upper band
            * lb: Lower band
            * mid: Midline
    """

    # Calculate the RSI
    rsi = talib.RSI(df[src], timeperiod=length)
    
    data = df[src]
    ep = 2 * length - 1
    auc = talib.EMA(pd.Series([max(data[i] - data[i-1], 0) for i in range(1, len(data))]), timeperiod=ep)
    adc = talib.EMA(pd.Series([max(data[i-1] - data[i], 0) for i in range(1, len(data))]), timeperiod=ep)
    x1 = (length - 1) * (adc * ob_level / (100 - ob_level) - auc)
    ub = pd.Series([data[i] + x1[i-1] if x1[i-1] >= 0 else data[i] + x1[i-1] * (100 - ob_level) / ob_level for i in range(1, len(data))])
    x2 = (length - 1) * (adc * os_level / (100 - os_level) - auc)
    lb = pd.Series([data[i] + x2[i-1] if x2[i-1] >= 0 else data[i] + x2[i-1] * (100 - os_level) / os_level for i in range(1, len(data))])


    # Return the DataFrame with the results
    return pd.DataFrame({"rsi": rsi, "ub": ub, "lb": lb, "mid":(ub + lb) / 2})
