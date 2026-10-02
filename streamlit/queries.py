# ============================================================
# CART2INSIGHTS
# SQL BUSINESS ANALYSIS QUERIES
# ============================================================

from database import run_query


# ============================================================
# 1. BUSINESS OVERVIEW
# ============================================================

def get_business_overview():

    query = """
        SELECT

            COUNT(
                DISTINCT o.order_id
            ) AS total_orders,

            COUNT(
                DISTINCT c.customer_unique_id
            ) AS total_customers,

            COUNT(
                DISTINCT oi.seller_id
            ) AS total_sellers,

            COALESCE(
                SUM(
                    oi.price + oi.freight_value
                ),
                0
            ) AS total_revenue,

            COALESCE(
                AVG(
                    order_values.order_value
                ),
                0
            ) AS average_order_value,

            COALESCE(
                (
                    SELECT AVG(
                        r.review_score
                    )
                    FROM order_reviews r
                ),
                0
            ) AS average_review_score

        FROM orders o

        JOIN customers c
            ON o.customer_id = c.customer_id

        LEFT JOIN order_items oi
            ON o.order_id = oi.order_id

        LEFT JOIN (

            SELECT

                order_id,

                SUM(
                    price + freight_value
                ) AS order_value

            FROM order_items

            GROUP BY order_id

        ) order_values

            ON o.order_id = order_values.order_id
    """

    return run_query(query)


# ============================================================
# 2. MONTHLY REVENUE TREND
# ============================================================

def get_monthly_revenue():

    query = """
        SELECT

            DATE_FORMAT(
                o.order_purchase_timestamp,
                '%Y-%m'
            ) AS month,

            SUM(
                oi.price + oi.freight_value
            ) AS revenue,

            COUNT(
                DISTINCT o.order_id
            ) AS orders,

            COUNT(
                DISTINCT c.customer_unique_id
            ) AS customers

        FROM orders o

        JOIN customers c
            ON o.customer_id = c.customer_id

        JOIN order_items oi
            ON o.order_id = oi.order_id

        GROUP BY month

        ORDER BY month
    """

    return run_query(query)


# ============================================================
# 3. REVENUE BY PRODUCT CATEGORY
# ============================================================

def get_revenue_by_category():

    query = """
        SELECT

            COALESCE(
                p.product_category_name,
                'Unknown'
            ) AS category,

            SUM(
                oi.price + oi.freight_value
            ) AS revenue,

            SUM(
                oi.price
            ) AS product_revenue,

            SUM(
                oi.freight_value
            ) AS freight_revenue,

            COUNT(*) AS units_sold,

            COUNT(
                DISTINCT oi.order_id
            ) AS orders

        FROM order_items oi

        JOIN products p
            ON oi.product_id = p.product_id

        GROUP BY category

        ORDER BY revenue DESC
    """

    return run_query(query)


# ============================================================
# 4. TOP-SELLING PRODUCTS
# ============================================================

def get_top_products(limit=10):

    limit = max(
        1,
        min(int(limit), 100)
    )

    query = f"""
        SELECT

            oi.product_id,

            COALESCE(
                p.product_category_name,
                'Unknown'
            ) AS category,

            SUM(
                oi.price
            ) AS revenue,

            SUM(
                oi.freight_value
            ) AS freight_revenue,

            COUNT(*) AS units_sold,

            COUNT(
                DISTINCT oi.order_id
            ) AS orders

        FROM order_items oi

        JOIN products p
            ON oi.product_id = p.product_id

        GROUP BY
            oi.product_id,
            category

        ORDER BY revenue DESC

        LIMIT {limit}
    """

    return run_query(query)


# ============================================================
# 5. SALES BY CUSTOMER LOCATION
# ============================================================

def get_sales_by_location():

    query = """
        SELECT

            c.customer_state AS state,

            COUNT(
                DISTINCT o.order_id
            ) AS orders,

            COUNT(
                DISTINCT c.customer_unique_id
            ) AS customers,

            SUM(
                oi.price + oi.freight_value
            ) AS revenue,

            AVG(
                oi.price + oi.freight_value
            ) AS average_item_value

        FROM orders o

        JOIN customers c
            ON o.customer_id = c.customer_id

        JOIN order_items oi
            ON o.order_id = oi.order_id

        GROUP BY c.customer_state

        ORDER BY revenue DESC
    """

    return run_query(query)


# ============================================================
# 6. CUSTOMER DISTRIBUTION
# ============================================================

def get_customer_distribution():

    query = """
        SELECT

            c.customer_state AS state,

            COUNT(
                DISTINCT c.customer_unique_id
            ) AS customers,

            COUNT(
                DISTINCT o.order_id
            ) AS orders,

            SUM(
                oi.price + oi.freight_value
            ) AS spending

        FROM customers c

        JOIN orders o
            ON c.customer_id = o.customer_id

        JOIN order_items oi
            ON o.order_id = oi.order_id

        GROUP BY c.customer_state

        ORDER BY customers DESC
    """

    return run_query(query)


# ============================================================
# 7. REPEAT VS ONE-TIME CUSTOMERS
# ============================================================

def get_repeat_customers():

    query = """
        SELECT

            customer_type,

            COUNT(*) AS customers

        FROM (

            SELECT

                c.customer_unique_id,

                COUNT(
                    DISTINCT o.order_id
                ) AS order_count,

                CASE

                    WHEN COUNT(
                        DISTINCT o.order_id
                    ) > 1

                    THEN 'Repeat Customer'

                    ELSE 'One-time Customer'

                END AS customer_type

            FROM customers c

            JOIN orders o
                ON c.customer_id = o.customer_id

            GROUP BY c.customer_unique_id

        ) customer_data

        GROUP BY customer_type

        ORDER BY customers DESC
    """

    return run_query(query)


# ============================================================
# 8. TOP CUSTOMERS
# ============================================================

def get_top_customers(limit=10):

    limit = max(
        1,
        min(int(limit), 100)
    )

    query = f"""
        SELECT

            c.customer_unique_id,

            COUNT(
                DISTINCT o.order_id
            ) AS order_count,

            SUM(
                oi.price + oi.freight_value
            ) AS total_spending,

            AVG(
                order_values.order_value
            ) AS average_order_value

        FROM customers c

        JOIN orders o
            ON c.customer_id = o.customer_id

        JOIN order_items oi
            ON o.order_id = oi.order_id

        LEFT JOIN (

            SELECT

                order_id,

                SUM(
                    price + freight_value
                ) AS order_value

            FROM order_items

            GROUP BY order_id

        ) order_values

            ON o.order_id = order_values.order_id

        GROUP BY c.customer_unique_id

        ORDER BY total_spending DESC

        LIMIT {limit}
    """

    return run_query(query)


# ============================================================
# 9. SELLER PERFORMANCE
# ============================================================

def get_seller_performance():

    query = """
        SELECT

            oi.seller_id,

            COUNT(
                DISTINCT oi.order_id
            ) AS order_count,

            COUNT(*) AS items_sold,

            SUM(
                oi.price
            ) AS seller_revenue,

            AVG(
                oi.price
            ) AS average_item_price

        FROM order_items oi

        GROUP BY oi.seller_id

        ORDER BY seller_revenue DESC
    """

    return run_query(query)


# ============================================================
# 10. TOP SELLERS
# ============================================================

def get_top_sellers(limit=10):

    limit = max(
        1,
        min(int(limit), 100)
    )

    query = f"""
        SELECT

            oi.seller_id,

            COUNT(
                DISTINCT oi.order_id
            ) AS order_count,

            COUNT(*) AS items_sold,

            SUM(
                oi.price
            ) AS seller_revenue

        FROM order_items oi

        GROUP BY oi.seller_id

        ORDER BY seller_revenue DESC

        LIMIT {limit}
    """

    return run_query(query)


# ============================================================
# 11. PRODUCT CATEGORY PERFORMANCE
# ============================================================

def get_category_performance():

    query = """
        SELECT

            COALESCE(
                p.product_category_name,
                'Unknown'
            ) AS category,

            COUNT(
                DISTINCT p.product_id
            ) AS products,

            COUNT(*) AS units_sold,

            SUM(
                oi.price
            ) AS revenue,

            AVG(
                oi.price
            ) AS average_price

        FROM products p

        JOIN order_items oi
            ON p.product_id = oi.product_id

        GROUP BY category

        ORDER BY revenue DESC
    """

    return run_query(query)


# ============================================================
# 12. SELLER RANKING USING WINDOW FUNCTION
# ============================================================

def get_seller_ranking():

    query = """
        WITH seller_revenue AS (

            SELECT

                seller_id,

                SUM(price) AS revenue

            FROM order_items

            GROUP BY seller_id

        )

        SELECT

            seller_id,

            revenue,

            RANK() OVER (
                ORDER BY revenue DESC
            ) AS revenue_rank

        FROM seller_revenue

        ORDER BY revenue_rank
    """

    return run_query(query)


# ============================================================
# 13. TOP CATEGORIES USING WINDOW FUNCTION
# ============================================================

def get_category_ranking():

    query = """
        WITH category_revenue AS (

            SELECT

                COALESCE(
                    p.product_category_name,
                    'Unknown'
                ) AS category,

                SUM(
                    oi.price
                ) AS revenue

            FROM order_items oi

            JOIN products p
                ON oi.product_id = p.product_id

            GROUP BY category

        )

        SELECT

            category,

            revenue,

            RANK() OVER (
                ORDER BY revenue DESC
            ) AS revenue_rank

        FROM category_revenue

        ORDER BY revenue_rank
    """

    return run_query(query)


# ============================================================
# 14. DELIVERY PERFORMANCE
# ============================================================

def get_delivery_performance():

    query = """
        SELECT

            CASE

                WHEN
                    o.order_delivered_customer_date
                    >
                    o.order_estimated_delivery_date

                THEN 'Delayed'

                ELSE 'On Time'

            END AS delivery_status,

            COUNT(
                DISTINCT o.order_id
            ) AS orders,

            AVG(
                TIMESTAMPDIFF(
                    DAY,
                    o.order_purchase_timestamp,
                    o.order_delivered_customer_date
                )
            ) AS average_delivery_days

        FROM orders o

        WHERE

            o.order_delivered_customer_date IS NOT NULL

            AND o.order_estimated_delivery_date IS NOT NULL

        GROUP BY delivery_status

        ORDER BY orders DESC
    """

    return run_query(query)


# ============================================================
# 15. DELIVERY PERFORMANCE BY LOCATION
# ============================================================

def get_delivery_by_location():

    query = """
        SELECT

            c.customer_state AS state,

            COUNT(
                DISTINCT o.order_id
            ) AS orders,

            AVG(
                TIMESTAMPDIFF(
                    DAY,
                    o.order_purchase_timestamp,
                    o.order_delivered_customer_date
                )
            ) AS average_delivery_days,

            AVG(
                CASE

                    WHEN
                        o.order_delivered_customer_date
                        >
                        o.order_estimated_delivery_date

                    THEN TIMESTAMPDIFF(
                        DAY,
                        o.order_estimated_delivery_date,
                        o.order_delivered_customer_date
                    )

                    ELSE 0

                END
            ) AS average_delay_days

        FROM orders o

        JOIN customers c
            ON o.customer_id = c.customer_id

        WHERE

            o.order_delivered_customer_date IS NOT NULL

            AND o.order_estimated_delivery_date IS NOT NULL

        GROUP BY c.customer_state

        ORDER BY average_delivery_days DESC
    """

    return run_query(query)


# ============================================================
# 16. DELIVERY DELAY VS REVIEW SCORE
# ============================================================

def get_delivery_review_analysis():

    query = """
        SELECT

            CASE

                WHEN
                    o.order_delivered_customer_date
                    >
                    o.order_estimated_delivery_date

                THEN 'Delayed'

                ELSE 'On Time'

            END AS delivery_status,

            AVG(
                r.review_score
            ) AS average_review_score,

            COUNT(*) AS review_count

        FROM order_reviews r

        JOIN orders o
            ON r.order_id = o.order_id

        WHERE

            o.order_delivered_customer_date IS NOT NULL

            AND o.order_estimated_delivery_date IS NOT NULL

        GROUP BY delivery_status
    """

    return run_query(query)


# ============================================================
# 17. REVIEW SCORE DISTRIBUTION
# ============================================================

def get_review_score_distribution():

    query = """
        SELECT

            review_score,

            COUNT(*) AS review_count,

            ROUND(
                COUNT(*) * 100.0
                /
                (
                    SELECT COUNT(*)
                    FROM order_reviews
                ),
                2
            ) AS percentage

        FROM order_reviews

        GROUP BY review_score

        ORDER BY review_score
    """

    return run_query(query)


# ============================================================
# 18. REVIEWS BY PRODUCT CATEGORY
# ============================================================

def get_reviews_by_category():

    query = """
        SELECT

            COALESCE(
                p.product_category_name,
                'Unknown'
            ) AS category,

            COUNT(
                DISTINCT r.review_id
            ) AS reviews,

            AVG(
                r.review_score
            ) AS average_review_score

        FROM order_reviews r

        JOIN order_items oi
            ON r.order_id = oi.order_id

        JOIN products p
            ON oi.product_id = p.product_id

        GROUP BY category

        ORDER BY average_review_score DESC
    """

    return run_query(query)


# ============================================================
# 19. PAYMENT METHOD ANALYSIS
# ============================================================

def get_payment_method_analysis():

    query = """
        SELECT

            payment_type,

            COUNT(
                DISTINCT order_id
            ) AS orders,

            SUM(
                payment_value
            ) AS payment_value,

            AVG(
                payment_value
            ) AS average_payment_value

        FROM order_payments

        GROUP BY payment_type

        ORDER BY payment_value DESC
    """

    return run_query(query)


# ============================================================
# 20. PAYMENT METHOD VS ORDER STATUS
# ============================================================

def get_payment_order_status():

    query = """
        SELECT

            p.payment_type,

            o.order_status,

            COUNT(
                DISTINCT o.order_id
            ) AS orders

        FROM order_payments p

        JOIN orders o
            ON p.order_id = o.order_id

        GROUP BY
            p.payment_type,
            o.order_status

        ORDER BY
            p.payment_type,
            orders DESC
    """

    return run_query(query)


# ============================================================
# 21. ORDER STATUS ANALYSIS
# ============================================================

def get_order_status_analysis():

    query = """
        SELECT

            order_status,

            COUNT(
                DISTINCT order_id
            ) AS orders,

            ROUND(
                COUNT(
                    DISTINCT order_id
                ) * 100.0
                /
                (
                    SELECT COUNT(
                        DISTINCT order_id
                    )
                    FROM orders
                ),
                2
            ) AS percentage

        FROM orders

        GROUP BY order_status

        ORDER BY orders DESC
    """

    return run_query(query)


# ============================================================
# 22. AVERAGE ORDER VALUE
# ============================================================

def get_average_order_value():

    query = """
        WITH order_values AS (

            SELECT

                order_id,

                SUM(
                    price + freight_value
                ) AS order_value

            FROM order_items

            GROUP BY order_id

        )

        SELECT

            AVG(
                order_value
            ) AS average_order_value,

            MIN(
                order_value
            ) AS minimum_order_value,

            MAX(
                order_value
            ) AS maximum_order_value

        FROM order_values
    """

    return run_query(query)


# ============================================================
# 23. CUSTOMER SPENDING SEGMENTS
# ============================================================

def get_customer_spending_segments():

    query = """
        WITH customer_spending AS (

            SELECT

                c.customer_unique_id,

                SUM(
                    oi.price + oi.freight_value
                ) AS total_spending

            FROM customers c

            JOIN orders o
                ON c.customer_id = o.customer_id

            JOIN order_items oi
                ON o.order_id = oi.order_id

            GROUP BY c.customer_unique_id
        )

        SELECT

            CASE

                WHEN total_spending < 100
                    THEN 'Low Spending'

                WHEN total_spending < 500
                    THEN 'Medium Spending'

                ELSE 'High Spending'

            END AS spending_segment,

            COUNT(*) AS customers,

            AVG(
                total_spending
            ) AS average_spending

        FROM customer_spending

        GROUP BY spending_segment

        ORDER BY average_spending
    """

    return run_query(query)


# ============================================================
# 24. MONTHLY CUSTOMER GROWTH
# ============================================================

def get_monthly_customer_growth():

    query = """
        SELECT

            DATE_FORMAT(
                o.order_purchase_timestamp,
                '%Y-%m'
            ) AS month,

            COUNT(
                DISTINCT c.customer_unique_id
            ) AS active_customers,

            COUNT(
                DISTINCT o.order_id
            ) AS orders

        FROM orders o

        JOIN customers c
            ON o.customer_id = c.customer_id

        GROUP BY month

        ORDER BY month
    """

    return run_query(query)


# ============================================================
# 25. MONTHLY DELIVERY PERFORMANCE
# ============================================================

def get_monthly_delivery_performance():

    query = """
        SELECT

            DATE_FORMAT(
                o.order_purchase_timestamp,
                '%Y-%m'
            ) AS month,

            AVG(
                TIMESTAMPDIFF(
                    DAY,
                    o.order_purchase_timestamp,
                    o.order_delivered_customer_date
                )
            ) AS average_delivery_days,

            AVG(
                CASE

                    WHEN
                        o.order_delivered_customer_date
                        >
                        o.order_estimated_delivery_date

                    THEN 1

                    ELSE 0

                END
            ) * 100 AS delayed_percentage

        FROM orders o

        WHERE

            o.order_delivered_customer_date IS NOT NULL

            AND o.order_estimated_delivery_date IS NOT NULL

        GROUP BY month

        ORDER BY month
    """

    return run_query(query)


# ============================================================
# 26. BUSINESS SUMMARY
# ============================================================

def get_business_summary():

    overview = get_business_overview()

    delivery = get_delivery_performance()

    reviews = get_review_score_distribution()

    return {
        "overview": overview,
        "delivery": delivery,
        "reviews": reviews
    }


# ============================================================
# 27. RUN ALL MAIN DASHBOARD QUERIES
# ============================================================

def get_dashboard_data():

    return {

        "business_overview":
            get_business_overview(),

        "monthly_revenue":
            get_monthly_revenue(),

        "revenue_by_category":
            get_revenue_by_category(),

        "top_products":
            get_top_products(10),

        "sales_by_location":
            get_sales_by_location(),

        "customer_distribution":
            get_customer_distribution(),

        "repeat_customers":
            get_repeat_customers(),

        "top_customers":
            get_top_customers(10),

        "seller_performance":
            get_seller_performance(),

        "top_sellers":
            get_top_sellers(10),

        "category_performance":
            get_category_performance(),

        "seller_ranking":
            get_seller_ranking(),

        "category_ranking":
            get_category_ranking(),

        "delivery_performance":
            get_delivery_performance(),

        "delivery_by_location":
            get_delivery_by_location(),

        "delivery_review":
            get_delivery_review_analysis(),

        "review_distribution":
            get_review_score_distribution(),

        "reviews_by_category":
            get_reviews_by_category(),

        "payment_methods":
            get_payment_method_analysis(),

        "payment_order_status":
            get_payment_order_status(),

        "order_status":
            get_order_status_analysis(),

        "average_order_value":
            get_average_order_value(),

        "customer_segments":
            get_customer_spending_segments(),

        "monthly_customer_growth":
            get_monthly_customer_growth(),

        "monthly_delivery":
            get_monthly_delivery_performance()
    }


# ============================================================
# TEST QUERY MODULE
# ============================================================

if __name__ == "__main__":

    print(
        "Testing Cart2Insights SQL query module..."
    )

    overview = get_business_overview()

    print("\nBusiness Overview:")
    print(overview)

    monthly = get_monthly_revenue()

    print("\nMonthly Revenue:")
    print(monthly.head())

    categories = get_revenue_by_category()

    print("\nRevenue by Category:")
    print(categories.head())

    sellers = get_top_sellers(5)

    print("\nTop Sellers:")
    print(sellers)

    customers = get_top_customers(5)

    print("\nTop Customers:")
    print(customers)

    delivery = get_delivery_performance()

    print("\nDelivery Performance:")
    print(delivery)

    reviews = get_review_score_distribution()

    print("\nReview Distribution:")
    print(reviews)

    print(
        "\n✅ queries.py test completed successfully"
    )