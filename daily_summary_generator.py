from summarizer import summarize_threat

def generate_daily_summary(log_file="daily_alerts.log", summary_file="daily_summary.txt"):
    try:
        with open(log_file, "r") as f:
            alerts = f.readlines()
    except FileNotFoundError:
        print("No alerts log found.")
        return

    summaries = []
    for alert_text in alerts[-20:]:  # summarize last 20 alerts only for brevity
        alert_dict = {"description": alert_text.strip()}
        summary = summarize_threat(alert_dict)
        summaries.append(summary)

    with open(summary_file, "w") as f:
        f.write("ShadowSentinel Daily Alert Summary\n\n")
        for i, s in enumerate(summaries, 1):
            f.write(f"{i}. {s}\n")

    print(f"Daily summary written to {summary_file}")

if __name__ == "__main__":
    generate_daily_summary()
