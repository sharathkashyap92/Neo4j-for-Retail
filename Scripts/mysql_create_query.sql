CREATE TABLE ITEM (
    item VARCHAR(50) PRIMARY KEY
);

CREATE TABLE AGG (
    item_name VARCHAR(50),
    user_id VARCHAR(20),
    count INT,
    PRIMARY KEY (item_name, user_id)
);


SELECT item.item AS Recommendation, count(1) AS Frequency
FROM item, agg, (SELECT agg3.item_name, agg3.user_id
    FROM agg agg, agg agg2, agg agg3
    WHERE agg.user_id = "18710"
    AND agg.item_name = agg2.item_name
    AND agg2.user_id != "18710"
    AND agg3.user_id = agg2.user_id
    AND agg3.user_id NOT IN (SELECT DISTINCT item_name
    FROM  agg agg
    WHERE agg.user_id = "18710")
    ) recommended_products
WHERE agg.item_name = item.item
AND agg.item_name IN (recommended_products.item_name)
AND agg.user_id = recommended_products.user_id
GROUP BY item.item
ORDER BY Frequency DESC
LIMIT 50;