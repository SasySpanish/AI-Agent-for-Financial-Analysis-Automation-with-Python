import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def run_comparative_viz(cleaned_files, session_dir):
    """
    Genera tutti i grafici comparativi per il report, caricando preferenzialmente
    i file con le features se disponibili.
    """
    plots_dir = os.path.join(session_dir, "plots")
    os.makedirs(plots_dir, exist_ok=True)

    # Preferiamo i file con le features calcolate
    feature_paths = {}
    for ticker, clean_path in cleaned_files.items():
        feat_path = os.path.join(session_dir, "features", f"{ticker}_features.csv")
        if os.path.exists(feat_path):
            feature_paths[ticker] = feat_path
        else:
            feature_paths[ticker] = clean_path
            print(f"   [viz] Features non trovate per {ticker} → uso cleaned")

    dfs = {}
    for ticker, path in feature_paths.items():
        try:
            df = pd.read_csv(path, parse_dates=['Date']).set_index('Date')
            dfs[ticker] = df
        except Exception as e:
            print(f"Errore caricamento {ticker}: {e}")

    if not dfs:
        print("Nessun dato valido da visualizzare.")
        return

    colors = sns.color_palette("husl", len(dfs))

    # 1. Prezzi di chiusura
    plt.figure(figsize=(13, 6.5))
    for i, (ticker, df) in enumerate(dfs.items()):
        col = 'Adj_Close' if 'Adj_Close' in df.columns else 'Close'
        plt.plot(df.index, df[col], label=ticker, color=colors[i], linewidth=1.9, alpha=0.9)

    plt.title("Confronto Prezzi di Chiusura", fontsize=15, pad=12)
    plt.xlabel("Data", fontsize=11)
    plt.ylabel("Prezzo ($)", fontsize=11)
    plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=10)
    plt.grid(True, alpha=0.2, linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "price_comparison.png"), dpi=320, bbox_inches='tight')
    plt.close()

    # 2. Ritorni logaritmici cumulativi
    plt.figure(figsize=(13, 6.5))
    for i, (ticker, df) in enumerate(dfs.items()):
        log_ret = np.log(df['Close'] / df['Close'].shift(1))
        cum_log = log_ret.cumsum() * 100
        plt.plot(cum_log.index, cum_log, label=ticker, color=colors[i], linewidth=2.0, alpha=0.92)

    plt.title("Ritorni Logaritmici Cumulativi (%)", fontsize=15, pad=12)
    plt.xlabel("Data", fontsize=11)
    plt.ylabel("Rendimento cumulativo log (%)", fontsize=11)
    plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=10)
    plt.grid(True, alpha=0.2, linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "cum_log_returns.png"), dpi=320, bbox_inches='tight')
    plt.close()

    # 3. RSI_14 comparativo
    plt.figure(figsize=(13, 6.5))
    plotted_rsi = False
    for i, (ticker, df) in enumerate(dfs.items()):
        if 'RSI_14' in df.columns:
            plt.plot(df.index, df['RSI_14'], label=ticker, color=colors[i], linewidth=1.8, alpha=0.9)
            plotted_rsi = True

    if plotted_rsi:
        plt.axhline(70, color='red', linestyle='--', alpha=0.5, linewidth=1.0)
        plt.axhline(30, color='lime', linestyle='--', alpha=0.5, linewidth=1.0)
        plt.ylim(0, 100)

    plt.title("RSI (14 giorni) Comparativo", fontsize=15, pad=12)
    plt.xlabel("Data", fontsize=11)
    plt.ylabel("RSI", fontsize=11)
    plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=10)
    plt.grid(True, alpha=0.2, linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "rsi_comparative.png"), dpi=320, bbox_inches='tight')
    plt.close()

    # 4. Volatilità rolling 20 giorni
    plt.figure(figsize=(13, 6.5))
    plotted_vol = False
    for i, (ticker, df) in enumerate(dfs.items()):
        if 'Volatility_20' in df.columns:
            plt.plot(df.index, df['Volatility_20'], label=ticker, color=colors[i], linewidth=1.9, alpha=0.9)
            plotted_vol = True

    plt.title("Volatilità Rolling 20 giorni (annualizzata)", fontsize=15, pad=12)
    plt.xlabel("Data", fontsize=11)
    plt.ylabel("Volatilità (%)", fontsize=11)
    plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=10)
    plt.grid(True, alpha=0.2, linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "volatility_20_comparative.png"), dpi=320, bbox_inches='tight')
    plt.close()

    # 5. Larghezza Bollinger Bands %
    plt.figure(figsize=(13, 6.5))
    plotted_bb = False
    for i, (ticker, df) in enumerate(dfs.items()):
        if all(col in df.columns for col in ['BB_Upper_20', 'BB_Lower_20', 'BB_Middle_20']):
            bb_width = (df['BB_Upper_20'] - df['BB_Lower_20']) / df['BB_Middle_20'] * 100
            plt.plot(df.index, bb_width, label=ticker, color=colors[i], linewidth=1.9, alpha=0.9)
            plotted_bb = True

    plt.title("Larghezza Bollinger Bands (20 gg) in %", fontsize=15, pad=12)
    plt.xlabel("Data", fontsize=11)
    plt.ylabel("BB Width (%)", fontsize=11)
    plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=10)
    plt.grid(True, alpha=0.2, linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "bollinger_width_comparative.png"), dpi=320, bbox_inches='tight')
    plt.close()

    print("📊 Grafici generati:")
    print("   • price_comparison.png")
    print("   • cum_log_returns.png")
    print("   • rsi_comparative.png"         + (" [OK]" if plotted_rsi else " [vuoto]"))
    print("   • volatility_20_comparative.png" + (" [OK]" if plotted_vol else " [vuoto]"))
    print("   • bollinger_width_comparative.png" + (" [OK]" if plotted_bb else " [vuoto]"))