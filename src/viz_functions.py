import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================
# 1. BASE CHARTS
# ============================================================

def plot_close_price(df, save_path=None):
    plt.figure(figsize=(10,5))
    plt.plot(df['Date'], df['Close'], color='steelblue', label='Close')
    plt.title('Closing Price Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.close()


def plot_volume(df, save_path=None):
    plt.figure(figsize=(10,4))
    plt.bar(df['Date'], df['Volume'], color='gray')
    plt.title('Trading Volume Over Time')
    plt.xlabel('Date')
    plt.ylabel('Volume')
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.close()


def plot_returns(df, save_path=None):
    plt.figure(figsize=(10,5))
    plt.plot(df['Date'], df['Return_Daily'], label='Daily', alpha=0.7)
    plt.plot(df['Date'], df['Return_Weekly'], label='Weekly', alpha=0.7)
    plt.plot(df['Date'], df['Return_Monthly'], label='Monthly', alpha=0.7)
    plt.title('Returns Over Time')
    plt.xlabel('Date')
    plt.ylabel('Return')
    plt.legend()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.close()


# ============================================================
# 2. TECHNICAL INDICATORS
# ============================================================

def plot_moving_averages(df, save_path=None):
    plt.figure(figsize=(10,5))
    plt.plot(df['Date'], df['Close'], color='black', label='Close', alpha=0.6)
    for window in [5,10,20]:
        plt.plot(df['Date'], df[f'SMA_{window}'], label=f'SMA {window}')
        plt.plot(df['Date'], df[f'EMA_{window}'], linestyle='--', label=f'EMA {window}')
    plt.title('Moving Averages (SMA & EMA)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.close()


def plot_bollinger_bands(df, save_path=None):
    plt.figure(figsize=(10,5))
    plt.plot(df['Date'], df['Close'], color='blue', label='Close')
    plt.plot(df['Date'], df['BB_Upper_20'], color='red', linestyle='--', label='Upper Band')
    plt.plot(df['Date'], df['BB_Lower_20'], color='green', linestyle='--', label='Lower Band')
    plt.fill_between(df['Date'], df['BB_Lower_20'], df['BB_Upper_20'], color='gray', alpha=0.1)
    plt.title('Bollinger Bands (20-day)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.close()


def plot_rsi(df, save_path=None):
    plt.figure(figsize=(10,4))
    plt.plot(df['Date'], df['RSI_14'], color='purple', label='RSI (14)')
    plt.axhline(70, color='red', linestyle='--', label='Overbought')
    plt.axhline(30, color='green', linestyle='--', label='Oversold')
    plt.title('RSI (Relative Strength Index)')
    plt.xlabel('Date')
    plt.ylabel('RSI')
    plt.legend()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.close()


def plot_macd(df, save_path=None):
    plt.figure(figsize=(10,5))
    plt.plot(df['Date'], df['MACD'], label='MACD', color='orange')
    plt.plot(df['Date'], df['MACD_Signal'], label='Signal', color='blue')
    plt.fill_between(df['Date'], df['MACD']-df['MACD_Signal'], 0, color='gray', alpha=0.2)
    plt.title('MACD Indicator')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.close()


# ============================================================
# 3. PERFORMANCE & RISK
# ============================================================

def plot_cumulative_returns(df, save_path=None):
    df['Cumulative_Return'] = (1 + df['Return_Daily']).cumprod()
    plt.figure(figsize=(10,5))
    plt.plot(df['Date'], df['Cumulative_Return'], color='navy')
    plt.title('Cumulative Returns')
    plt.xlabel('Date')
    plt.ylabel('Growth of 1 Unit')
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.close()


def plot_drawdown(df, save_path=None):
    df['Cumulative_Return'] = (1 + df['Return_Daily']).cumprod()
    df['Cumulative_Max'] = df['Cumulative_Return'].cummax()
    df['Drawdown'] = (df['Cumulative_Return'] - df['Cumulative_Max']) / df['Cumulative_Max']
    plt.figure(figsize=(10,4))
    plt.fill_between(df['Date'], df['Drawdown'], 0, color='red', alpha=0.3)
    plt.title('Drawdown Over Time')
    plt.xlabel('Date')
    plt.ylabel('Drawdown')
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.close()


def plot_volatility(df, save_path=None):
    plt.figure(figsize=(10,5))
    for window in [5,10,20]:
        plt.plot(df['Date'], df[f'Volatility_{window}'], label=f'Volatility {window}')
    plt.title('Rolling Volatility')
    plt.xlabel('Date')
    plt.ylabel('Volatility')
    plt.legend()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.close()


# ============================================================
# 4. STATISTICAL ANALYSIS
# ============================================================

def plot_return_distribution(df, save_path=None):
    plt.figure(figsize=(8,4))
    sns.histplot(df['Return_Daily'], bins=50, kde=True, color='steelblue')
    plt.title('Distribution of Daily Returns')
    plt.xlabel('Return')
    plt.ylabel('Frequency')
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.close()


def plot_correlation_heatmap(df, save_path=None):
    plt.figure(figsize=(10,8))
    corr = df.select_dtypes(include='number').corr()
    sns.heatmap(corr, cmap='coolwarm', center=0)
    plt.title('Feature Correlation Heatmap')
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.close()


# ============================================================
# 5. INTERACTIVE VISUALS (Plotly)
# ============================================================

def interactive_candlestick(df, save_path=None):
    fig = go.Figure(data=[go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    )])
    fig.update_layout(title='Interactive Candlestick Chart', xaxis_rangeslider_visible=False)
    if save_path:
        fig.write_html(save_path)
    return fig


def interactive_macd(df, save_path=None):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3])
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Close'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MACD'], name='MACD'), row=2, col=1)
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MACD_Signal'], name='Signal'), row=2, col=1)
    fig.update_layout(title='Interactive MACD Indicator')
    if save_path:
        fig.write_html(save_path)
    return fig
