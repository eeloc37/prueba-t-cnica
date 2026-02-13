CREATE OR REPLACE VIEW vw_daily_company_amount AS
SELECT
    DATE(ch.created_at) AS transaction_date,
    co.company_id,
    co.company_name,
    SUM(ch.amount) AS total_amount
FROM charges ch
JOIN companies co
    ON ch.company_id = co.company_id
GROUP BY
    DATE(ch.created_at),
    co.company_id,
    co.company_name;

SELECT * FROM vw_daily_company_amount ORDER BY transaction_date, company_name;