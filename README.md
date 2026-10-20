# Acquisition Funnel Insights

**Status: in progress**

An analysis of an acquisition funnel for a B2B online service, from first website visit to paying customer. The goal is to show non-technical teams where prospects drop off, which channels bring the best customers, and what to do about it.

## Why this project

Marketing and sales teams spend money on many channels (search ads, social ads, partnerships, referrals). Without a clear funnel view, it is hard to know which channels really bring customers who stay. This project turns raw event data into a simple dashboard and clear recommendations.

## How it works

1. Generate a realistic dataset of website visits, sign-ups, account activations and paid subscriptions (simulated data).
2. Write SQL queries to calculate conversion rates at each step, by channel and by month.
3. Compare channels on cost per acquisition and activation rate.
4. Build a Looker Studio dashboard for business teams.
5. Write a short summary with 3 concrete recommendations.

## Tech stack

SQL, Python (pandas), Looker Studio

## Progress

- [ ] Funnel definition and metrics
- [x] Simulated dataset
- [ ] SQL analysis by step and by channel
- [ ] Looker Studio dashboard
- [ ] Summary and recommendations

## Planned structure

```
acquisition-funnel-insights/
  data/
    generate_data.py
  sql/
    funnel_by_channel.sql
    conversion_by_month.sql
  notebooks/
    analysis.ipynb
  reports/
    summary.md
  README.md
```

## Author

Saiteja Eleti - [LinkedIn](https://www.linkedin.com/in/saiteja-eleti-169028332/)
