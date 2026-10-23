SELECT segment, COUNT(*) AS customers,
SUM(conversion) AS conversions,
ROUND(AVG(conversion), 5) AS conversion_rate,
ROUND(AVG(visit), 5) AS visit_rate,
ROUND(AVG(spend), 3) AS revenue_per_customer
FROM customers GROUP BY segment;

SELECT channel, segment, COUNT(*) AS customers,
ROUND(AVG(conversion), 5) AS conversion_rate
FROM customers GROUP BY channel, segment;

WITH rates AS (
SELECT newbie, segment, AVG(conversion) AS rate, COUNT(*) AS n
FROM customers
WHERE segment IN ('Mens E-Mail', 'No E-Mail')
GROUP BY newbie, segment
)
SELECT a.newbie, a.n AS treated, b.n AS control,
ROUND(a.rate-b.rate, 5) AS conversion_difference
FROM rates a JOIN rates b ON a.newbie=b.newbie
WHERE a.segment='Mens E-Mail' AND b.segment='No E-Mail';
