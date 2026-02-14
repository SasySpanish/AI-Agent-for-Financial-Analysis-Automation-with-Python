import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from eda_functions import convert_numeric, summary_statistics


def run_comparative_eda(cleaned_files, session_dir):
    """
    Esegue l'EDA comparativa tra più asset
    Crea un summary leggero e ben strutturato per il report
    """
    print("   Caricamento e pulizia dati...")

    dfs = {}
    for ticker, path in cleaned_files.items():
        print(f"   → {ticker}")
        df = pd.read_csv(path, parse_dates=['Date'])
        df = convert_numeric(df)

        # Pulizia aggressiva ma sicura
        for col in ['Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume']:
            if col in df.columns:
                df[col] = pd.to_numeric(
                    df[col].astype(str).str.replace(',', '').str.strip(),
                    errors='coerce'
                )

        dfs[ticker] = df

    # =============================================
    #          CREAZIONE SUMMARY PER REPORT
    # =============================================
    report_rows = []

    for ticker, df in dfs.items():
        if df.empty:
            print(f"   ⚠️  Nessun dato valido per {ticker}")
            continue

        # colonne che ci interessano
        focus_cols = ['Date', 'Close', 'Volume']
        focus = df[focus_cols].dropna(subset=['Date', 'Close']).copy()

        if focus.empty:
            continue

        # statistiche di base
        stats = focus.describe(percentiles=[0.5])

        for stat_name in ['min', '50%', 'max']:
            row = {
                'Ticker': ticker,
                'Statistica': stat_name,
                'Date': stats.loc[stat_name, 'Date'].strftime('%Y-%m-%d'),
                'Close': round(stats.loc[stat_name, 'Close'], 2),
                'Volume': round(stats.loc[stat_name, 'Volume'], 0)   # volume intero
            }
            report_rows.append(row)

    # =============================================
    #           Salvataggio summary leggero
    # =============================================
    if report_rows:
        summary_df = pd.DataFrame(report_rows)
        summary_path = os.path.join(session_dir, "reports", "summary_comparative.csv")
        summary_df.to_csv(summary_path, index=False, encoding='utf-8')
        print(f"   ✅ Summary leggero salvato → {summary_path}")
    else:
        print("   ⚠️  Nessun dato valido per creare il summary")

    # =============================================
    #               GRAFICO CORRELAZIONE
    # =============================================
    if len(dfs) >= 2:
        print("   Creazione matrice di correlazione...")
        prices = pd.DataFrame({
            ticker: df.set_index('Date')['Close']
            for ticker, df in dfs.items()
        })

        returns = prices.pct_change(fill_method=None).dropna(how='all')

        if not returns.empty:
            corr = returns.corr()

            plt.figure(figsize=(10, 8))
            sns.heatmap(
                corr,
                annot=True,
                cmap="coolwarm",
                fmt=".2f",
                linewidths=0.6,
                square=True,
                cbar_kws={'shrink': .8}
            )
            plt.title("Correlazione tra Rendimenti Giornalieri")
            plt.tight_layout()
            plt.savefig(
                os.path.join(session_dir, "plots", "correlation_matrix.png"),
                dpi=300,
                bbox_inches='tight'
            )
            plt.close()
            print("   ✓ Matrice di correlazione salvata")
        else:
            print("   ⚠️  Non abbastanza dati per calcolare la correlazione")

    print("\n✅ EDA comparativa completata!")