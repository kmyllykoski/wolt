-- Wolt 
-- Assigment Task 2 - Top 5 countries by average order value
-- Average order value = value of sales in country / number of orders in country
--
-- Author: KM
-- SQL: PostgreSQL 15

SELECT 
    c.country,
    SUM(c.count) AS order_volume, 
    ROUND(SUM(c.order_line_sales_total_ex_vat_eur)::numeric, 2) AS sales_per_country_ex_vat_eur,
    ROUND(SUM(c.order_line_margin_ex_vat_eur)::numeric, 2) AS total_margin_per_country_ex_vat_eur,
    ROUND((SUM(c.order_line_margin_ex_vat_eur) / SUM(c.order_line_sales_total_ex_vat_eur)
          * 100)::numeric, 1) AS margin_perc,
    COUNT(*) AS order_lines_count,
    COUNT(DISTINCT(c.purchase_id)) AS purchase_count,
    ROUND((SUM(c.order_line_sales_total_ex_vat_eur) / COUNT(DISTINCT(c.purchase_id)))::numeric, 2) AS avg_order_value,  
    ROUND(SUM(c.count) / COUNT(DISTINCT(c.purchase_id))::numeric, 1) AS avg_order_size
          
FROM
(       SELECT 
            pi.product_id,
            pi.purchase_id,       
            pi.count,
            pi.venue_id,
            pi.baseprice,
            pi.vat_percentage,
            i.cost_per_unit_eur,
            i.cost_per_unit,
            baseprice_inc_vat_eur,
            baseprice_ex_vat_eur,
            baseprice_ex_vat_eur * pi.count as order_line_sales_total_ex_vat_eur, 
            baseprice_ex_vat_eur - i.cost_per_unit_eur as item_margin_per_item_ex_vat_eur,
            (baseprice_ex_vat_eur - i.cost_per_unit_eur) * pi.count as order_line_margin_ex_vat_eur,
            country
                
        FROM purchase_item AS pi       
              
        INNER JOIN LATERAL(
            SELECT * FROM item
            WHERE item.product_id = pi.product_id and
                  item.venue_id = pi.venue_id and
                  item.cost_per_unit IS NOT NULL and
                  item.cost_per_unit_eur IS NOT NULL and
                  available_date < (SELECT time_received FROM purchase WHERE purchase_id = pi.purchase_id)
            ORDER BY available_date DESC NULLS LAST
            LIMIT 1
        ) i ON TRUE
    
        CROSS JOIN LATERAL (
            SELECT 
            
                -- Calculating sales price in EUR based on the relation between cost_per_unit in local
                -- currency and cost_per_unit in EUR available in item data.
                -- If data for eur or local cost is missing then CASE returns zero because these both
                -- are used to get the exchange rate for converting sales price in local currency to eur.
                --
                -- Baseprice being zero will lead to order line being skipped in the WHERE clause below.
            
                (CASE WHEN i.cost_per_unit_eur > 0 and i.cost_per_unit > 0 -- and i.cost_per_unit IS NOT NULL
                    THEN (i.cost_per_unit_eur/i.cost_per_unit) * pi.baseprice
                    ELSE 0
                    END) as baseprice_inc_vat_eur,  
            
                -- Calculating price excluding VAT
                (CASE WHEN i.cost_per_unit_eur > 0 and i.cost_per_unit > 0
                    THEN (i.cost_per_unit_eur/i.cost_per_unit) * pi.baseprice
                    ELSE 0
                    END) / (1 + (pi.vat_percentage/100)) as baseprice_ex_vat_eur,
                    
                -- Get country where order was made from purchase table
                (SELECT country FROM purchase WHERE purchase_id = pi.purchase_id),
            
                -- Get time when order was received from customer
                (SELECT time_received FROM purchase WHERE purchase_id = pi.purchase_id)
        ) as z
 
        WHERE pi.count > 0 and -- data has orders lines with zero items, these order lines will be skipped here
              baseprice_inc_vat_eur > 0 
) as c

GROUP BY c.country 
ORDER BY SUM(c.order_line_sales_total_ex_vat_eur) / COUNT(DISTINCT(c.purchase_id)) DESC
LIMIT 5

