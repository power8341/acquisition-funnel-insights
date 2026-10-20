-- How long between account opening and first transaction (median and 90th percentile, in days)?
WITH opened AS (
    SELECT visitor_id, MIN(CAST(event_at AS TIMESTAMP)) AS opened_at FROM funnel_events
    WHERE step = 'account_opened' GROUP BY visitor_id
),
activated AS (
    SELECT visitor_id, MIN(CAST(event_at AS TIMESTAMP)) AS activated_at FROM funnel_events
    WHERE step = 'activated' GROUP BY visitor_id
)
SELECT v.channel,
       COUNT(*)                                                                                   AS activated_customers,
       ROUND(MEDIAN(DATE_DIFF('hour', o.opened_at, a.activated_at)) / 24.0, 1)                    AS median_days,
       ROUND(QUANTILE_CONT(DATE_DIFF('hour', o.opened_at, a.activated_at), 0.9) / 24.0, 1)        AS p90_days
FROM opened o
JOIN activated a USING (visitor_id)
JOIN visitors v USING (visitor_id)
GROUP BY v.channel
ORDER BY median_days;
