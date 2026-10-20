"""Check the SQL logic on a tiny hand-made dataset where the right answer is known."""
from pathlib import Path

import duckdb

SQL = Path(__file__).resolve().parent.parent / "sql"


def tiny_db():
    con = duckdb.connect()
    con.execute("CREATE TABLE visitors (visitor_id INT, channel TEXT, device TEXT, first_visit_at TEXT)")
    con.execute("CREATE TABLE funnel_events (visitor_id INT, step TEXT, event_at TEXT)")
    con.execute("CREATE TABLE channel_spend (month TEXT, channel TEXT, spend_eur DOUBLE)")
    # 4 SEO visitors: 2 start, 1 completes, 1 opens, 1 activates
    con.execute("""INSERT INTO visitors VALUES
        (1,'SEO','desktop','2026-05-02 10:00:00'), (2,'SEO','mobile','2026-05-03 10:00:00'),
        (3,'SEO','mobile','2026-05-04 10:00:00'), (4,'SEO','desktop','2026-05-05 10:00:00')""")
    con.execute("""INSERT INTO funnel_events VALUES
        (1,'visit','2026-05-02 10:00:00'),(2,'visit','2026-05-03 10:00:00'),
        (3,'visit','2026-05-04 10:00:00'),(4,'visit','2026-05-05 10:00:00'),
        (1,'signup_started','2026-05-02 10:05:00'),(2,'signup_started','2026-05-03 10:05:00'),
        (1,'signup_completed','2026-05-02 10:20:00'),(1,'account_opened','2026-05-03 10:20:00'),
        (1,'activated','2026-05-05 10:20:00')""")
    con.execute("INSERT INTO channel_spend VALUES ('2026-05-01','SEO',100)")
    return con


def run(name):
    return tiny_db().execute((SQL / name).read_text()).df()


def test_funnel_counts_and_rates():
    row = run("01_funnel_by_channel.sql").iloc[0]
    assert (row.visits, row.signup_started, row.signup_completed, row.account_opened, row.activated) == (4, 2, 1, 1, 1)
    assert row.pct_visit_to_start == 50.0 and row.pct_start_to_complete == 50.0


def test_cost_per_activated():
    row = run("02_channel_efficiency.sql").iloc[0]
    assert row.cost_per_activated_eur == 100.0 and row.activation_rate_pct == 100.0


def test_device_dropoff():
    df = run("04_device_dropoff.sql").set_index("device")
    assert df.loc["desktop", "pct_start_to_complete"] == 100.0
    assert df.loc["mobile", "pct_start_to_complete"] == 0.0


def test_time_to_activation_is_two_days():
    assert run("05_time_to_activation.sql").iloc[0].median_days == 2.0
