-- Where do mobile and desktop users drop off in the sign-up form?
SELECT v.device,
       COUNT(DISTINCT CASE WHEN e.step = 'signup_started'   THEN e.visitor_id END) AS signup_started,
       COUNT(DISTINCT CASE WHEN e.step = 'signup_completed' THEN e.visitor_id END) AS signup_completed,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN e.step = 'signup_completed' THEN e.visitor_id END)
             / NULLIF(COUNT(DISTINCT CASE WHEN e.step = 'signup_started' THEN e.visitor_id END), 0), 1)
                                                                                    AS pct_start_to_complete
FROM visitors v
JOIN funnel_events e ON e.visitor_id = v.visitor_id
GROUP BY v.device
ORDER BY v.device;
