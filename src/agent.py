import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import ollama
from download_clean import download_and_clean_multiple
from eda_comparative import run_comparative_eda
from viz_comparative import run_comparative_viz
from feature_engineering import run_feature_engineering
from report_generator import generate_html_report

# ──────────────────────────────────────────────────────────────
# Nuova funzione per generare mini-grafici
# ──────────────────────────────────────────────────────────────

def generate_mini_plots(files_dict, session_dir, use_features=True):
    from eda_functions import plot_price_trend  # importiamo la funzione base
    
    mini_dir = os.path.join(session_dir, "plots", "mini")
    os.makedirs(mini_dir, exist_ok=True)
    
    print("   Generazione mini-grafici per il report...")
    
    for ticker, path in files_dict.items():
        try:
            df = pd.read_csv(path, parse_dates=['Date'])
            if df.empty:
                continue
               
            # Usiamo una versione più piccola e senza troppi fronzoli
            save_path = os.path.join(mini_dir, f"mini_{ticker}.png")
            
            plt.figure(figsize=(5.2, 2.8))
            plt.style.use("dark_background")
            plt.plot(df['Date'], df['Close'], color='#00d4ff', linewidth=1.4)
            plt.title(ticker, fontsize=11, pad=6)
            plt.xticks([])
            plt.yticks(fontsize=9)
            plt.grid(alpha=0.15, linestyle='--')
            plt.tight_layout(pad=0.6)
            plt.savefig(save_path, dpi=180, bbox_inches='tight')
            plt.close()
            
            print(f"     ✓ mini_{ticker}.png creato")
            
        except Exception as e:
            print(f"     ⚠️ Errore mini-grafico {ticker}: {e}")

# ──────────────────────────────────────────────────────────────

def query_qwen(prompt: str, system: str = "") -> str:
    response = ollama.chat(
        model='qwen2.5:3b',
        messages=[
            {'role': 'system', 'content': system},
            {'role': 'user', 'content': prompt}
        ]
    )
    return response['message']['content'].strip()

def parse_user_prompt(user_prompt: str):
    system = """
    Sei un esperto di mercati finanziari. Analizza il prompt e rispondi SOLO con JSON valido:
    {
      "assets_type": "commodities" | "stocks" | "other",
      "number": numero intero,
      "criteria": "top" | "bottom" | "best_performing" | "recent",
      "features_requested": true/false
    }
    Usa solo ticker validi di Yahoo Finance.
    """
    try:
        json_str = query_qwen(user_prompt, system)
        return json.loads(json_str)
    except:
        return {"assets_type": "stocks", "number": 5, "criteria": "top", "features_requested": False}

def get_tickers(parsed):
    if parsed["assets_type"] == "commodities":
        return ["GC=F", "SI=F", "CL=F", "NG=F", "HG=F"][:parsed["number"]]
    
    elif parsed["assets_type"] == "stocks":
        top_sp500 = ["NVDA", "AAPL", "MSFT", "AMZN", "GOOGL", "META", "AVGO", "TSLA", "BRK-B", "LLY", "JPM", "V", "XOM", "UNH", "MA"]
        if parsed["criteria"] in ["top", "best_performing"]:
            return top_sp500[:parsed["number"]]
        else:
            try:
                df = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
                return df["Symbol"].tolist()[:parsed["number"]]
            except:
                return top_sp500[:parsed["number"]]
    return ["GC=F"]  # default

def main():
    user_prompt = input("\n🤖 Inserisci il tuo prompt (es. 'vorrei informazioni sulle top5 materie prime'): ")
    
    print("🧠 Qwen2.5-3B sta analizzando il prompt...")
    parsed = parse_user_prompt(user_prompt)
    print(f"   → Tipo: {parsed['assets_type']}, N: {parsed['number']}, Features: {parsed.get('features_requested', False)}")
    
    tickers = get_tickers(parsed)
    print(f"📌 Asset selezionati: {tickers}")
    
    # Cartella sessione
    session_name = f"{user_prompt[:50].replace(' ', '_').replace('?', '')}_{datetime.now().strftime('%Y%m%d_%H%M')}"
    session_dir = os.path.join("analyses", session_name)
    for d in ["data", "reports", "plots", "features"]:
        os.makedirs(os.path.join(session_dir, d), exist_ok=True)
    
    # Fase 1: Download + pulizia
    print("\n📥 Fase 1: Download + pulizia...")
    cleaned_files = download_and_clean_multiple(tickers, session_dir)
    
    # Fase 2: EDA comparativa (summary + correlation matrix)
    print("\n🔍 Fase 2: EDA comparativa...")
    run_comparative_eda(cleaned_files, session_dir)
    
    # Fase 3: Calcolo delle feature tecniche (RSI, BB, Volatility, ecc.)
    print("\n🛠️ Fase 3: Calcolo indicatori tecnici...")
    feature_files = {}
    run_feature_engineering(cleaned_files, session_dir)
    
    # Creiamo un dizionario con preferenza per i file con features
    for ticker, clean_path in cleaned_files.items():
        feat_path = os.path.join(session_dir, "features", f"{ticker}_features.csv")
        if os.path.exists(feat_path):
            feature_files[ticker] = feat_path
        else:
            feature_files[ticker] = clean_path
            print(f"   ⚠️  Features non trovate per {ticker} → uso cleaned")
    
    # Fase 4: Mini-grafici per il report
    print("\n🖼️ Fase 4: Creazione mini-grafici per summary...")
    generate_mini_plots(feature_files, session_dir)
    
    # Fase 5: Visualizzazioni comparative (ora con features)
    print("\n📊 Fase 5: Visualizzazioni comparative...")
    run_comparative_viz(cleaned_files, session_dir)  # ← passeremo feature_files sotto
    
    # Fase 6: Report HTML
    print("\n📄 Fase 6: Generazione report HTML...")
    generate_html_report(session_dir, tickers, user_prompt)
    
    print(f"\n✅ ANALISI COMPLETATA!")
    print(f"   📁 Cartella: analyses/{session_name}/")
    print(f"   🌐 Report: {os.path.join(session_dir, 'reports', 'report.html')}")

if __name__ == "__main__":
    main()