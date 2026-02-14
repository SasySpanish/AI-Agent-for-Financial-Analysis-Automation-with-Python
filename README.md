# AI Financial Reporter

This is a small Python tool that helps you quickly create nice financial reports.

You just write a simple sentence (like "show me the top 5 commodities" or "compare gold, silver and oil"), and the program:

- downloads the latest prices
- creates comparison charts
- calculates useful indicators (RSI, volatility, Bollinger Bands…)
- builds a beautiful HTML report with tables and graphs

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
- A bit of AI help to understand your question

Enjoy exploring markets visually and quickly!

MIT License
