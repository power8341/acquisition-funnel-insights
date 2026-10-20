-- Monthly visit-to-sign-up-started rate by channel, to spot changes over time.
SELECT DATE_TRUNC('month', CAST(v.first_visit_at AS TIMESTAMP))::DATE                      AS month,
       v.channel,
       COUNT(DISTINCT v.visitor_id)                                                        AS visits,
       COUNT(DISTINCT CASE WHEN e.step = 'signup_started' THEN e.visitor_id END)           AS signup_started,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN e.step = 'signup_started' THEN e.visitor_id END)
             / COUNT(DISTINCT v.visitor_id), 1)                                            AS pct_visit_to_start,
       COUNT(DISTINCT CASE WHEN e.step = 'activated' THEN e.visitor_id END)                AS activated
FROM visitors v
LEFT JOIN funnel_events e ON e.visitor_id = v.visitor_id
GROUP BY 1, 2
ORDER BY 2, 1;
