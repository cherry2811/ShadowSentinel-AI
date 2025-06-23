import json
import os
from datetime import datetime

LOG_FILE = "threat_log.json"

def update_threat_log(date, score):
    data = {}

    # Load old data
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}

    # Add or update today's entry
    data[date] = score

    # Keep only last 7 days sorted by date
    if len(data) > 7:
        sorted_items = sorted(data.items(), key=lambda x: x[0])[-7:]
        data = dict(sorted_items)

    # Save updated log
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def generate_dashboard(score, summary, blocked_ips):
    today = datetime.now().strftime("%Y-%m-%d")
    update_threat_log(today, score)  # Update log with today's score

    # Load graph data
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                score_data = json.load(f)
            except json.JSONDecodeError:
                score_data = {}
    else:
        score_data = {}

    dates = list(score_data.keys())
    scores = list(score_data.values())

    blocked_list = ", ".join(blocked_ips) if blocked_ips else "None"

    html = f"""
    <html>
    <head>
        <title>ShadowSentinel AI - Threat Dashboard</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{
                font-family: 'Segoe UI', sans-serif;
                background-color: #0d1117;
                color: #f0f6fc;
                padding: 40px;
            }}
            .card {{
                background-color: #161b22;
                border-radius: 16px;
                padding: 30px;
                box-shadow: 0 0 20px rgba(0,255,255,0.1);
                max-width: 800px;
                margin: auto;
            }}
            h1 {{
                color: #58a6ff;
                text-align: center;
            }}
            .score {{
                font-size: 48px;
                color: #00ff99;
                text-align: center;
                margin-bottom: 20px;
            }}
            .summary {{
                font-style: italic;
                color: #d2a8ff;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>ShadowSentinel Threat Report</h1>
            <div class="score">⚠️ Threat Score: <strong>{score}/100</strong></div>
            <p><strong>🗓️ Date:</strong> {today}</p>
            <p><strong>🚫 Blocked IPs:</strong> {blocked_list}</p>
            <p class="summary">🧠 {summary}</p>
            <div id="graph" style="margin-top:40px;"></div>
        </div>

        <script>
            var trace = {{
                x: {dates},
                y: {scores},
                type: 'scatter',
                mode: 'lines+markers',
                marker: {{ color: '#58a6ff' }},
                line: {{ shape: 'spline' }}
            }};

            var layout = {{
                title: '🧠 Last 7 Days Threat Score',
                paper_bgcolor: '#0d1117',
                plot_bgcolor: '#0d1117',
                font: {{ color: '#f0f6fc' }}
            }};

            Plotly.newPlot('graph', [trace], layout);
        </script>
    </body>
    </html>
    """
    with open("dashboard.html", "w") as f:
        f.write(html)

    print("✅ Dashboard with graph generated: dashboard.html")

# Example usage (remove or modify in your actual workflow)
if __name__ == "__main__":
    example_score = 42
    example_summary = "No major threats detected today."
    example_blocked_ips = ["192.168.1.101", "10.0.0.5"]
    generate_dashboard(example_score, example_summary, example_blocked_ips)

