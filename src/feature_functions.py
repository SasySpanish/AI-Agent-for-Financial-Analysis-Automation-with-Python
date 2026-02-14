import pandas as pd

# ============================================================
# FEATURE ENGINEERING PER GC=F (Oro)
# ============================================================

def compute_returns(df: pd.DataFrame) -> pd.DataFrame:
    """Calcola i rendimenti giornalieri, settimanali e mensili"""
    df = df.copy()
    
    df['Return_Daily']   = df['Close'].pct_change()
    df['Return_Weekly']  = df['Close'].pct_change(periods=5)   # 5 giorni di trading
    df['Return_Monthly'] = df['Close'].pct_change(periods=21)  # ~1 mese
    
    return df


def compute_moving_averages(df: pd.DataFrame) -> pd.DataFrame:
    """SMA ed EMA a 5, 10, 20 giorni"""
    df = df.copy()
    
    for window in [5, 10, 20]:
        df[f'SMA_{window}'] = df['Close'].rolling(window=window).mean()
        df[f'EMA_{window}'] = df['Close'].ewm(span=window, adjust=False).mean()
    
    return df


def compute_volatility(df: pd.DataFrame) -> pd.DataFrame:
    """Volatilità rolling (std dei rendimenti) su 5, 10, 20 giorni"""
    df = df.copy()
    
    for window in [5, 10, 20]:
        df[f'Volatility_{window}'] = (
            df['Return_Daily'].rolling(window=window).std() * (252 ** 0.5)
        )  # annualizzata
    
    return df


def compute_RSI(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """Relative Strength Index"""
    df = df.copy()
    
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    
    rs = gain / loss
    df[f'RSI_{period}'] = 100 - (100 / (1 + rs))
    
    return df


def compute_MACD(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    """MACD + Signal + Histogram"""
    df = df.copy()
    
    ema_fast = df['Close'].ewm(span=fast, adjust=False).mean()
    ema_slow = df['Close'].ewm(span=slow, adjust=False).mean()
    
    df['MACD'] = ema_fast - ema_slow
    df['MACD_Signal'] = df['MACD'].ewm(span=signal, adjust=False).mean()
    df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
    
    return df


def compute_bollinger_bands(df: pd.DataFrame, window: int = 20, num_std: int = 2) -> pd.DataFrame:
    """Bollinger Bands (20, 2)"""
    df = df.copy()
    
    sma = df['Close'].rolling(window=window).mean()
    std = df['Close'].rolling(window=window).std()
    
    df[f'BB_Upper_{window}'] = sma + (std * num_std)
    df[f'BB_Lower_{window}'] = sma - (std * num_std)
    df[f'BB_Middle_{window}'] = sma  # opzionale ma utile
    
    return df


# ============================================================
# FUNZIONE COMODA PER CALCOLARE TUTTO IN UNA VOLTA
# ============================================================

def compute_all_features(df: pd.DataFrame) -> pd.DataFrame:
    """Esegue tutte le feature in sequenza (ordine corretto)"""
    df = df.copy()
    
    df = compute_returns(df)
    df = compute_moving_averages(df)
    df = compute_volatility(df)
    df = compute_RSI(df)
    df = compute_MACD(df)
    df = compute_bollinger_bands(df)
    
    # Rimuove le prime righe con NaN (causate dai rolling)
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    return df