-- Cost per account opened and per activated customer, by channel (whole period).
WITH results AS (
    SELECT v.channel,
           COUNT(DISTINCT CASE WHEN e.step = 'account_opened' THEN e.visitor_id END) AS accounts_opened,
           COUNT(DISTINCT CASE WHEN e.step = 'activated'      THEN e.visitor_id END) AS activated
    FROM visitors v
    JOIN funnel_events e ON e.visitor_id = v.visitor_id
    GROUP BY v.channel
),
costs AS (
    SELECT channel, SUM(spend_eur) AS spend_eur FROM channel_spend GROUP BY channel
)
SELECT r.channel,
       ROUND(c.spend_eur, 0)                                     AS spend_eur,
       r.accounts_opened,
       r.activated,
       ROUND(c.spend_eur / NULLIF(r.accounts_opened, 0), 1)      AS cost_per_account_eur,
       ROUND(c.spend_eur / NULLIF(r.activated, 0), 1)            AS cost_per_activated_eur,
       ROUND(100.0 * r.activated / NULLIF(r.accounts_opened, 0), 1) AS activation_rate_pct
FROM results r
JOIN costs c USING (channel)
ORDER BY cost_per_activated_eur;
