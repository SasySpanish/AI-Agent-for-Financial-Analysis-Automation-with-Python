import pandas as pd

def clean_financial_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pulisce e standardizza un dataset finanziario scaricato da Yahoo Finance.

    Passaggi:
    - Rimuove righe con valori mancanti.
    - Elimina duplicati.
    - Converte l'indice (Date) in colonna.
    - Ordina il dataset per data.
    - Rinomina le colonne in formato standard.
    """
    df = df.copy()

    # Rimuovi valori nulli e duplicati
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    # Se la data è l'indice, spostala in una colonna
    if isinstance(df.index, pd.DatetimeIndex):
        df.reset_index(inplace=True)

    # Assicurati che la colonna 'Date' sia in formato datetime
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values(by='Date', inplace=True)

    # Rinomina colonne in formato standard (senza spazi)
    rename_dict = {
        'Adj Close': 'Adj_Close'
    }
    df.rename(columns=rename_dict, inplace=True)

    # Riordina colonne se possibile
    expected_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume']
    df = df[[col for col in expected_cols if col in df.columns]]

    return df
