-- Wolt 
-- Assigment Task 1
-- Author: KM
-- SQL: PostgreSQL 15

SELECT 
    c.purchase_id,
    c.country,
    c.time_received::TIMESTAMP::DATE AS date_received, 
    SUM(c.count) AS number_of_items,
    ROUND(SUM(c.order_line_sales_total_ex_vat_eur)::numeric, 2) AS sales_per_purchase_ex_vat_eur,
    ROUND(SUM(c.order_line_margin_ex_vat_eur)::numeric, 2) AS margin_per_purchase_ex_vat_eur,
    ROUND((SUM(c.order_line_margin_ex_vat_eur) / SUM(c.order_line_sales_total_ex_vat_eur)
          * 100)::numeric, 1) AS margin_perc
           
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
            country,
            time_received
                
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
            
                (CASE WHEN i.cost_per_unit_eur > 0 and i.cost_per_unit > 0
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
 
        WHERE pi.count > 0 and -- order lines with zero items will be skipped here
              baseprice_inc_vat_eur > 0 
) as c

GROUP BY c.purchase_id, c.country, c.time_received
ORDER BY sum(c.order_line_margin_ex_vat_eur) DESC

