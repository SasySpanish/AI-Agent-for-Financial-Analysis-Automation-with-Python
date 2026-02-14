# AI Agent for Financial Analysis

This is a small Python tool that helps you quickly create nice financial reports.

This is a small Python tool that helps you quickly create nice financial reports.

### How it works (simple explanation)

Behind the scenes, the program follows these main steps:

1. You write your question in normal words  
   (example: "compare gold and silver" or "top 5 tech stocks performance")

2. A small local AI model (Qwen 2.5 3B running with Ollama) reads your sentence  
   → understands what you want  
   → chooses which companies or commodities to analyze

3. The program automatically downloads fresh price data  
   → uses Yahoo Finance (yfinance library)

4. It cleans the data  
   → removes errors, fixes formats, makes sure dates and numbers are correct

5. It does some quick analysis (EDA)  
   → calculates basic statistics  
   → creates a correlation matrix between assets

6. It calculates useful technical indicators  
   → RSI (overbought / oversold)  
   → Bollinger Bands  
   → rolling volatility  
   → cumulative returns  
   → moving averages, MACD, etc.

7. It creates clear comparison charts  
   → price trends side by side  
   → cumulative performance  
   → RSI comparison  
   → volatility comparison  
   → Bollinger Bands width

8. Finally, it builds a nice HTML report  
   → summary table for each asset (min / median / max)  
   → small preview chart for each asset  
   → big comparison charts  
   → everything opens in your browser

All of this happens in a few minutes, and every new request creates its own separate folder so nothing gets mixed up.

You don't need to write any code or open spreadsheets — just describe what you want to see.

Everything happens automatically — no need to open Excel or TradingView manually.

## What you can do with it

- Compare prices and performance of several stocks or commodities at once
- See which asset is more volatile right now
- Look at RSI, cumulative returns, Bollinger width side by side
- Get a clean report you can save or share

## Quick examples of what you can ask

- "I want a report on the top 5 commodities"
- "Compare NVDA, AAPL, MSFT and TSLA"
- "Gold vs silver vs crude oil in the last 3 years"
- "Show me the best performing big tech stocks"

## How to try it

1. Download or clone this repository
2. Install Python (if you don't have it already — version 3.9 or newer is fine)
3. Double-click (or run) the file called `src/agent.py`
4. When a box appears, just type your question and press Enter

The program will create a new folder inside `results/analyses/` with all the charts and the final HTML report.

You can open the report by double-clicking the file `report.html` — it should open in your browser.

## See some ready-made examples

Inside the folder `results/examples/` you can already find a few nice-looking reports:

- Major commodities (gold, silver, oil, gas, copper)
- Top US tech stocks
- Energy sector vs technology sector

Just open any `report.html` file there to see how the final result looks.

## Project folders explained

- `src/` → all the Python code files  
- `results/` → where new reports are saved  
- `results/examples/` → some beautiful ready-to-view reports

More details:

- [README-src.md](./README-src.md) → what each Python file does  
- [README-results.md](./README-results.md) → how to understand and use the generated reports

## Made with

- Python
- yfinance (to get market data)
- pandas, matplotlib, seaborn (for tables and charts)
- ollama qwen 2.5:3b as a LLM to help to understand the prompt

Enjoy exploring markets visually and quickly!

