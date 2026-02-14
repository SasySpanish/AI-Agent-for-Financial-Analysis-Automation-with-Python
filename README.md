# AI-Agent-for-Financial-Analysis-Automation-with-Python
# AI Financial Reporter

An automated Python agent that downloads financial data (stocks & commodities), computes technical indicators, generates comparative visualizations, and produces rich, well-formatted HTML reports — all starting from a simple natural language prompt.

## Features

- Natural language prompt (English or Italian supported) → automatic selection of assets (top commodities, big tech stocks, etc.)
- Data download & cleaning using **yfinance**
- Calculation of common technical indicators: RSI, MACD, Bollinger Bands, rolling volatility, cumulative log returns
- Multi-asset comparative charts: prices, cumulative returns, RSI, volatility, Bollinger Band width
- Responsive HTML reports including mini price charts, summary tables, and large comparative visuals
- Each analysis creates its own timestamped session folder (`analyses/`) containing: data, plots, reports, features

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/your-username/AI-Financial-Reporter.git
cd AI-Financial-Reporter

# 2. (Recommended) Create & activate virtual environment
python -m venv venv
source venv/bin/activate          # Linux / macOS
# venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the agent
python src/agent.py
```
Then type a prompt, for example:

- "I want a report on the top 5 commodities"
- "Comparative analysis NVDA AAPL MSFT TSLA"
- "Gold vs silver vs crude oil last 3 years"

### Requirements
- Python ≥ 3.9
- Main libraries:
- yfinance
- pandas
- numpy
- matplotlib
- seaborn
- jinja2
- ollama (used for natural language prompt parsing)
