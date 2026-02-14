import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------
# Funzioni EDA
# --------------------------

def load_data(file_path):
    """Load CSV into a pandas DataFrame"""
    df = pd.read_csv(file_path, parse_dates=["Date"])
    return df

def convert_numeric(df, columns=None):
    """Convert columns to numeric, ignoring errors"""
    if columns is None:
        columns = ['Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume']
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def summary_statistics(df):
    """Return basic descriptive statistics"""
    return df.describe()

def generate_summary(df, ticker=None, save_dir=None):
    """
    Genera un riassunto descrittivo del dataset e, se richiesto, lo salva su file CSV.
    """
    summary = df.describe(include='all').transpose()

    if ticker and save_dir:
        output_path = os.path.join(save_dir, f"{ticker}_summary.csv")
        summary.to_csv(output_path, index=True)
        print(f"✅ Summary salvato in: {output_path}")

    return summary

def plot_price_trend(df, ticker, save_dir):
    plt.style.use("dark_background")  # Style sicuro
    plt.figure(figsize=(10,5))
    plt.plot(df['Date'], df['Close'], label='Close')
    if 'Adj_Close' in df.columns:
        plt.plot(df['Date'], df['Adj_Close'], label='Adj Close')
    plt.title(f"{ticker} Price Trend")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f"{ticker}_trend.png"))
    plt.close()

def plot_distribution(df, ticker, save_dir):
    plt.style.use("dark_background")
    plt.figure(figsize=(12,5))
    plt.subplot(1,2,1)
    sns.histplot(df['Close'], kde=True)
    plt.title(f"{ticker} Close Price Histogram")
    plt.subplot(1,2,2)
    sns.boxplot(x=df['Close'])
    plt.title(f"{ticker} Close Price Boxplot")
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f"{ticker}_distribution.png"))
    plt.close()

def correlation_heatmap(df, ticker, save_dir):
    df = convert_numeric(df)
    corr = df.select_dtypes(include='number').corr()
    if corr.empty:
        print(f"No numeric columns for correlation heatmap for {ticker}, skipping.")
        return
    plt.figure(figsize=(8,6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title(f"{ticker} Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f"{ticker}_correlation.png"))
    plt.close()
