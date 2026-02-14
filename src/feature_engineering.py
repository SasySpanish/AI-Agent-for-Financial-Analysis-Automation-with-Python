import os
import pandas as pd
from feature_functions import compute_all_features  # usa la versione migliorata che ti ho dato prima

def run_feature_engineering(cleaned_files, session_dir):
    for ticker, path in cleaned_files.items():
        df = pd.read_csv(path)
        df = compute_all_features(df)
        df.to_csv(os.path.join(session_dir, "features", f"{ticker}_features.csv"), index=False)