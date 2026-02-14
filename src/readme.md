# Source Code Documentation (src/)

This folder contains all the Python scripts that make the **AI Financial Reporter** work.

Here is a short and clear explanation of what each file does.

### Main files

**agent.py**  
The heart of the program.  
This is the script you run to start everything.  
It:
- asks you for a question (the prompt)
- uses a small AI model to understand what assets you want to analyze
- coordinates all the other steps: download data → clean → analysis → charts → report
- creates a new folder for each analysis with date and time in the name

**report_generator.py**  
Builds the final HTML report that opens in your browser.  
It takes all the charts and tables created earlier, puts them together in a nice-looking page, adds colors and layout, and saves it as `report.html`.

**viz_comparative.py**  
Creates the big comparison charts that appear in the report.  
Examples:
- Prices of all assets together
- Cumulative returns
- RSI comparison
- Volatility comparison
- Bollinger Bands width comparison

These are the main graphs you see side by side for multiple assets.

**feature_engineering.py**  
Runs the calculations of technical indicators for each asset.  
It reads the cleaned data, adds columns like RSI, MACD, Bollinger Bands, volatility, moving averages, etc., and saves the enriched files in the `features/` folder.

**feature_functions.py**  
Contains the actual math functions used to calculate the indicators (RSI, MACD, Bollinger Bands, volatility, returns, etc.).  
It is called by `feature_engineering.py`.

**download_clean.py**  
Downloads fresh data from Yahoo Finance for the chosen tickers and cleans it a little before saving.  
It creates the first clean CSV files in the `data/` folder.

**data_cleaner.py**  
A small helper file that contains the cleaning rules used by `download_clean.py` (remove missing values, fix column names, make sure dates are correct, etc.).

**eda_comparative.py**  
Performs basic exploratory data analysis across all assets.  
It creates:
- a simple summary table (min, median, max for prices and volume)
- a correlation matrix between the assets' returns  
These are used in the report and for the correlation heatmap.

**eda_functions.py**  
Contains helper functions for single-asset EDA (used mainly in older or alternative parts of the code).  
Examples: plot price trend, volume bar chart, return distribution, correlation heatmap for one asset.

**viz_functions.py**  
Older or alternative visualization functions for single assets (candlestick, MACD, Bollinger Bands, drawdown, etc.).  
Most of them are not actively used in the current comparative version, but they are kept here in case you want to extend the tool later.

### Summary – quick overview

| File                        | Main job                                      | When it runs                  |
|-----------------------------|-----------------------------------------------|-------------------------------|
| `agent.py`                  | Runs everything, coordinates steps            | First (you start here)        |
| `download_clean.py`         | Downloads + basic cleaning                    | Step 1                        |
| `data_cleaner.py`           | Cleaning rules                                | Called by download_clean      |
| `eda_comparative.py`        | Summary stats + correlation matrix            | Step 2                        |
| `feature_engineering.py`    | Adds technical indicators                     | Step 3                        |
| `feature_functions.py`      | The actual indicator calculations             | Called by feature_engineering |
| `viz_comparative.py`        | Creates comparison charts (multi-asset)       | Step 5                        |
| `report_generator.py`       | Builds the final HTML report                  | Last step                     |
| `eda_functions.py`          | Single-asset EDA helpers (not main flow)      | Optional / legacy             |
| `viz_functions.py`          | Single-asset chart helpers (not main flow)    | Optional / legacy             |

All these files work together so that you only need to write a sentence and get a complete financial comparison report without touching the code.

Enjoy!
