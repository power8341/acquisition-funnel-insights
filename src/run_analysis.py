"""Run every SQL file on the funnel data and save results and charts.

Usage:
    python data/generate_data.py      # create the simulated data
    python -m src.run_analysis        # run the SQL, save CSVs and charts in reports/

The CSVs in reports/ are ready to upload to Google Sheets and connect to Looker Studio.
"""

from pathlib import Path

import duckdb
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA, SQL, REPORTS = ROOT / "data", ROOT / "sql", ROOT / "reports"


def connect():
    con = duckdb.connect()
    for table in ("visitors", "funnel_events", "channel_spend"):
        con.execute(f"CREATE TABLE {table} AS SELECT * FROM read_csv_auto('{DATA / (table + '.csv')}')")
    return con


def run_all(con):
    results = {}
    for sql_file in sorted(SQL.glob("*.sql")):
        df = con.execute(sql_file.read_text()).df()
        results[sql_file.stem] = df
        df.to_csv(REPORTS / f"{sql_file.stem}.csv", index=False)
        print(f"\n== {sql_file.stem} ==\n{df.to_string(index=False)}")
    return results


def charts(results):
    funnel = results["01_funnel_by_channel"].set_index("channel")
    steps = ["visits", "signup_started", "signup_completed", "account_opened", "activated"]
    ax = (funnel[steps].T / funnel["visits"] * 100).plot(marker="o", figsize=(8, 4.5))
    ax.set_yscale("log")
    ax.set_ylabel("% of visitors (log scale)")
    ax.set_title("Funnel by channel: share of visitors reaching each step")
    plt.tight_layout()
    plt.savefig(REPORTS / "funnel_by_channel.png", dpi=120)
    plt.close()

    eff = results["02_channel_efficiency"].set_index("channel")["cost_per_activated_eur"].sort_values()
    ax = eff.plot(kind="barh", figsize=(7, 4), color="#2b6cb0")
    ax.set_xlabel("Cost per activated customer (EUR)")
    ax.set_title("Which channels bring active customers at the best cost?")
    plt.tight_layout()
    plt.savefig(REPORTS / "cost_per_activated.png", dpi=120)
    plt.close()

    trend = results["03_monthly_trend"].pivot(index="month", columns="channel", values="pct_visit_to_start")
    ax = trend.plot(marker="o", figsize=(8, 4.5))
    ax.set_ylabel("Visit to sign-up started (%)")
    ax.set_title("Monthly trend: sign-up start rate by channel")
    plt.tight_layout()
    plt.savefig(REPORTS / "monthly_trend.png", dpi=120)
    plt.close()


def main():
    REPORTS.mkdir(exist_ok=True)
    con = connect()
    results = run_all(con)
    charts(results)
    print(f"\nSaved results and charts to {REPORTS}")


if __name__ == "__main__":
    main()
