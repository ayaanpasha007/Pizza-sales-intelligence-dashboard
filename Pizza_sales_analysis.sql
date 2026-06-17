USE company_db;
SELECT *
FROM pizza_sales
WHERE order_id IS NULL
   OR pizza_name IS NULL
   OR pizza_category IS NULL
   OR pizza_size IS NULL
   OR quantity IS NULL
   OR total_price IS NULL;
   
SELECT DISTINCT *
FROM pizza_sales;

SELECT order_date
FROM pizza_sales
LIMIT 10;

SELECT 
order_id,
order_date,
DAYNAME(STR_TO_DATE(order_date,'%d-%m-%Y')) AS day_name,
MONTHNAME(STR_TO_DATE(order_date,'%d-%m-%Y')) AS month_name
FROM pizza_sales;

SELECT 
SUM(total_price) AS total_revenue
FROM pizza_sales;

SELECT 
SUM(total_price) / COUNT(DISTINCT order_id) AS avg_order_value
FROM pizza_sales;

SELECT 
SUM(quantity) AS total_pizzas_sold
FROM pizza_sales;

SELECT 
COUNT(DISTINCT order_id) AS total_orders
FROM pizza_sales;


SELECT 
CAST(SUM(quantity) AS FLOAT) / COUNT(DISTINCT order_id) AS avg_pizzas_per_order
FROM pizza_sales;


-- daily trends
SELECT 
DAYNAME(STR_TO_DATE(order_date,'%d-%m-%Y')) AS order_day,
COUNT(DISTINCT order_id) AS total_orders
FROM pizza_sales
GROUP BY order_day
ORDER BY total_orders DESC;


-- monthly trends
SELECT 
MONTHNAME(STR_TO_DATE(order_date,'%d-%m-%Y')) AS month,
COUNT(DISTINCT order_id) AS total_orders
FROM pizza_sales
GROUP BY month
ORDER BY total_orders DESC;

-- PERCENTAGE OF SALES BY PIZZA CATEGORY
SELECT 
pizza_category,
SUM(total_price) AS revenue,
SUM(total_price) * 100 / (SELECT SUM(total_price) FROM pizza_sales) AS percentage
FROM pizza_sales
GROUP BY pizza_category
ORDER BY percentage  DESC;

-- PERCENTAGE OF SALES BY PIZZA SIZE (Pie Chart)
SELECT 
pizza_size,
SUM(total_price) AS revenue,
SUM(total_price) * 100 / (SELECT SUM(total_price) FROM pizza_sales) AS percentage
FROM pizza_sales
GROUP BY pizza_size;

-- TOTAL PIZZAS SOLD BY CATEGORY (Funnel Chart)
SELECT 
pizza_category,
SUM(quantity) AS total_pizzas_sold
FROM pizza_sales
GROUP BY pizza_category
ORDER BY total_pizzas_sold DESC;

-- Top 5 by Revenue
SELECT 
pizza_name,
SUM(total_price) AS revenue
FROM pizza_sales
GROUP BY pizza_name
ORDER BY revenue DESC
LIMIT 5;

-- Top 5 by Quantity
SELECT 
pizza_name,
SUM(quantity) AS total_quantity
FROM pizza_sales
GROUP BY pizza_name
ORDER BY total_quantity DESC
LIMIT 5;

-- Top 5 by Orders
SELECT 
pizza_name,
COUNT(order_id) AS total_orders
FROM pizza_sales
GROUP BY pizza_name
ORDER BY total_orders DESC
LIMIT 5;

-- BOTTOM 5 WORST SELLERS
-- Bottom 5 by Revenue
SELECT 
pizza_name,
SUM(total_price) AS revenue
FROM pizza_sales
GROUP BY pizza_name
ORDER BY revenue ASC
LIMIT 5;


-- Bottom 5 by Quantity
SELECT 
pizza_name,
SUM(quantity) AS total_quantity
FROM pizza_sales
GROUP BY pizza_name
ORDER BY total_quantity ASC
LIMIT 5;


-- Bottom 5 by Orders
SELECT 
pizza_name,
COUNT(order_id) AS total_orders
FROM pizza_sales
GROUP BY pizza_name
ORDER BY total_orders ASC
LIMIT 5;

