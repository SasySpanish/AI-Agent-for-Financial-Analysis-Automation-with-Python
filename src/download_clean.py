import yfinance as yf
import pandas as pd
import os
from data_cleaner import clean_financial_data

def download_and_clean_multiple(tickers, base_dir):
    cleaned = {}
    for ticker in tickers:
        print(f"   ↓ {ticker}")
        
        # Download
        data = yf.download(ticker, period="max", progress=False, auto_adjust=False)
        
        if data.empty:
            print(f"   ⚠️  Nessun dato per {ticker}")
            continue
        
        # ====================== FIX MULTIINDEX (il vero problema) ======================
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = [col[0] for col in data.columns]   # prende solo il primo livello
        
        # Normalizza nomi colonne (spazi, ecc.)
        data.columns = [str(col).replace(' ', '_') for col in data.columns]
        
        # Ora pulisci
        cleaned_data = clean_financial_data(data)
        
        # ====================== CONVERSIONE NUMERICA SICURA ======================
        numeric_cols = ['Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume']
        
        for col in numeric_cols:
            if col in cleaned_data.columns:
                series = cleaned_data[col]
                
                # Se per qualche motivo è ancora DataFrame → prendi prima colonna
                if isinstance(series, pd.DataFrame):
                    series = series.iloc[:, 0]
                
                # Conversione sicura
                cleaned_data[col] = pd.to_numeric(series, errors='coerce')
        
        # Salva
        path = os.path.join(base_dir, "data", f"{ticker}_cleaned.csv")
        cleaned_data.to_csv(path, index=False)
        cleaned[ticker] = path
        
        print(f"   ✅ {ticker} salvato ({len(cleaned_data):,} righe)")
    
    return cleaned