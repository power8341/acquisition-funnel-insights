-- Visitors reaching each funnel step, by channel, with step-to-step conversion rates.
WITH reached AS (
    SELECT v.channel,
           COUNT(DISTINCT v.visitor_id)                                                      AS visits,
           COUNT(DISTINCT CASE WHEN e.step = 'signup_started'   THEN e.visitor_id END)       AS signup_started,
           COUNT(DISTINCT CASE WHEN e.step = 'signup_completed' THEN e.visitor_id END)       AS signup_completed,
           COUNT(DISTINCT CASE WHEN e.step = 'account_opened'   THEN e.visitor_id END)       AS account_opened,
           COUNT(DISTINCT CASE WHEN e.step = 'activated'        THEN e.visitor_id END)       AS activated
    FROM visitors v
    LEFT JOIN funnel_events e ON e.visitor_id = v.visitor_id
    GROUP BY v.channel
)
SELECT channel, visits, signup_started, signup_completed, account_opened, activated,
       ROUND(100.0 * signup_started   / NULLIF(visits, 0), 1)           AS pct_visit_to_start,
       ROUND(100.0 * signup_completed / NULLIF(signup_started, 0), 1)   AS pct_start_to_complete,
       ROUND(100.0 * account_opened   / NULLIF(signup_completed, 0), 1) AS pct_complete_to_opened,
       ROUND(100.0 * activated        / NULLIF(account_opened, 0), 1)   AS pct_opened_to_activated,
       ROUND(100.0 * activated        / NULLIF(visits, 0), 2)           AS pct_visit_to_activated
FROM reached
ORDER BY activated DESC;
