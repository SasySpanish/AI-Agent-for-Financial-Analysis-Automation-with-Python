import os
from datetime import datetime
from jinja2 import Template
import pandas as pd
import matplotlib.pyplot as plt
import base64


def image_to_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')
    except Exception:
        return ""


def generate_html_report(session_dir, tickers, user_prompt):
    report_dir = os.path.join(session_dir, "reports")
    plots_dir = os.path.join(session_dir, "plots")
    features_dir = os.path.join(session_dir, "features")

    os.makedirs(report_dir, exist_ok=True)

    # Immagini principali (tutti i comparativi)
    main_images = []
    for fname in [
        "price_comparison.png",
        "cum_log_returns.png",
        "rsi_comparative.png",
        "volatility_20_comparative.png",
        "bollinger_width_comparative.png",
        "correlation_matrix.png"
    ]:
        full_path = os.path.join(plots_dir, fname)
        if os.path.exists(full_path):
            b64 = image_to_base64(full_path)
            if b64:
                main_images.append({
                    'filename': fname,
                    'title': fname.replace('_', ' ').title().replace('Comparative', 'Comparativo'),
                    'base64': b64
                })

    # Mini-grafici per tabelle (se già implementato)
    mini_plots = {}
    mini_dir = os.path.join(plots_dir, "mini")
    if os.path.exists(mini_dir):
        for ticker in tickers:
            mini_path = os.path.join(mini_dir, f"mini_{ticker}.png")
            if os.path.exists(mini_path):
                b64 = image_to_base64(mini_path)
                if b64:
                    mini_plots[ticker] = b64

    # Tabelle summary per asset
    summary_path = os.path.join(report_dir, "summary_comparative.csv")
    table_dict = {}

    if os.path.exists(summary_path):
        df = pd.read_csv(summary_path)
        df = df.reset_index(drop=True)

        stat_col = df.columns[0]
        if 'Statistica' not in df.columns:
            df = df.rename(columns={stat_col: 'Statistica'})

        wanted = ['min', '50%', 'max']
        df_filtered = df[df['Statistica'].isin(wanted)].reset_index(drop=True)

        rename_map = {
            'Data':   'Data (range)',
            'Close':  'Close ($)',
            'Volume': 'Volume'
        }
        df_filtered = df_filtered.rename(columns=rename_map)

        if 'Ticker' in df_filtered.columns:
            for ticker in tickers:
                subset = df_filtered[df_filtered['Ticker'] == ticker]
                if not subset.empty:
                    table_dict[ticker] = subset.to_html(
                        index=False,
                        classes="compact-asset-table",
                        float_format="%.2f",
                        na_rep="–",
                        border=0,
                        justify="left"
                    )

    # ────────────────────────────── TEMPLATE HTML ──────────────────────────────
    html_template = """
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Report • {{ user_prompt }}</title>
        <style>
            body { font-family: 'Segoe UI', system-ui, sans-serif; background: #0a0a0a; color: #e0e0e0; margin: 0; padding: 35px 20px; line-height: 1.45; }
            h1 { color: #00ff9d; text-align: center; margin-bottom: 0.3em; }
            h2 { color: #00cc7a; margin: 1.2em 0 0.6em; }
            h3 { color: #00e68a; margin: 1.8em 0 0.8em; }
            h4 { color: #88ffcc; margin: 0.4em 0 0.8em; font-size: 1.15em; }
            .container { max-width: 1320px; margin: auto; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(460px, 1fr)); gap: 20px; margin: 1.8em 0; }
            .card { background: #161616; padding: 18px; border-radius: 10px; box-shadow: 0 6px 20px rgba(0,0,0,0.55); }
            img.main-chart { max-width: 100%; border-radius: 8px; box-shadow: 0 5px 16px rgba(0,0,0,0.5); }
            .footer { text-align: center; margin-top: 3.5em; color: #555; font-size: 0.88em; }

            /* Layout tabella + mini-grafico (se implementato) */
            .asset-container { display: flex; flex-direction: column; gap: 1.4em; margin-top: 1.2em; }
            .asset-row { display: flex; align-items: flex-start; gap: 1.8em; background: #1a1a1a; padding: 14px; border-radius: 10px; border: 1px solid #252525; }
            .asset-table { flex: 1 1 45%; min-width: 240px; }
            .asset-chart { flex: 0 0 340px; text-align: right; }
            .mini-chart { max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 3px 10px rgba(0,0,0,0.5); background: #111; }
            .no-chart { color: #777; font-style: italic; padding: 30px 10px; text-align: center; background: #222; border-radius: 8px; }

            .compact-asset-table th, .compact-asset-table td { text-align: left !important; padding: 5px 8px; border-bottom: 1px solid #252525; }
            .compact-asset-table th { background: #1e1e1e; color: #aaffdd; font-weight: 500; }
            .compact-asset-table tr:last-child td { border-bottom: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Report Finanziario</h1>
            <h2>{{ user_prompt | title }}</h2>
            <p><strong>Data analisi:</strong> {{ now }}</p>
            <p><strong>Asset:</strong> {{ tickers | join(', ') }}</p>

            <!-- Tabelle + mini-grafici -->
            <div class="card">
                <h3>Riepilogo per asset (min / mediana / max)</h3>
                <div class="asset-container">
                    {% for ticker in tickers %}
                    <div class="asset-row">
                        <div class="asset-table">
                            <h4>{{ ticker }}</h4>
                            {% if table_dict[ticker] %}
                                {{ table_dict[ticker] | safe }}
                            {% else %}
                                <p style="color:#ff7777;">Dati non disponibili</p>
                            {% endif %}
                        </div>
                        <div class="asset-chart">
                            {% if mini_plots[ticker] %}
                            <img src="data:image/png;base64,{{ mini_plots[ticker] }}" alt="Andamento {{ ticker }}" class="mini-chart">
                            {% else %}
                            <div class="no-chart">Grafico non disponibile</div>
                            {% endif %}
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <!-- Grafici comparativi principali -->
            <div class="grid">
                {% for img in main_images %}
                <div class="card">
                    <h3>{{ img.title }}</h3>
                    <img src="data:image/png;base64,{{ img.base64 }}" alt="{{ img.filename }}" class="main-chart">
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="footer">
            Generato automaticamente • {{ now }}
        </div>
    </body>
    </html>
    """

    template = Template(html_template)
    html_content = template.render(
        user_prompt=user_prompt,
        tickers=tickers,
        main_images=main_images,
        table_dict=table_dict,
        mini_plots=mini_plots,
        now=datetime.now().strftime("%d %B %Y • %H:%M")
    )

    report_path = os.path.join(report_dir, "report.html")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Report HTML generato con tutti i grafici comparativi")
    print(f"   📍 {report_path}")
    return report_path