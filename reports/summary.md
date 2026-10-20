# Acquisition funnel: summary for business teams

Period: May to October 2026. Data: simulated funnel of 263,000 website visitors for a B2B online business account (not real company data).

## Key findings

**1. Referral and SEO bring active customers at a fraction of the cost of paid ads.**
Cost per activated customer: Referral 30 EUR, SEO 36 EUR, Partnerships 81 EUR, Paid Search 147 EUR, Paid Social 305 EUR. Paid Social costs 10 times more than Referral for one active customer.

**2. Paid Social brings sign-ups that do not become active.**
Only 39% of accounts opened from Paid Social make a first transaction, against 54% to 71% for the other channels. The August landing page change raised the sign-up start rate from about 9% to 11%, but it did not fix the quality of these sign-ups.

**3. The mobile sign-up form loses more people.**
51.5% of mobile users who start signing up finish, against 60.2% on desktop. Bringing mobile to the desktop level would mean about 1,150 more completed sign-ups over six months, with no extra ad spend.

**4. Activation takes time.**
Customers make their first transaction about 10 days after opening their account (median), and 10% take more than 19 days. The first week after account opening is the moment to help them.

## Recommendations

1. **Move part of the Paid Social budget to Referral and Partnerships**, and test a referral reward. Measure cost per activated customer, not cost per sign-up.
2. **Fix the mobile sign-up form first**: find the field where mobile users leave (form analytics), simplify it, and A/B test the new version.
3. **Add an activation journey in the first 7 days** (email or in-app at day 3 and day 7) showing the first useful action, and track the effect on the 30-day activation rate.

## How these numbers were produced

SQL queries in `sql/`, run with DuckDB by `src/run_analysis.py`. Result tables are in `reports/*.csv` and charts in `reports/*.png`.
