use test_join

SELECT *
FROM products p
INNER JOIN categories c ON c.category_id = p.category_id
-- INNER JOIN brands b ON b.brand_id = p.brand_id

