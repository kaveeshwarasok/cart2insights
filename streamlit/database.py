# ============================================================
# CART2INSIGHTS
# DATABASE CONNECTION & DATABASE UTILITIES
# ============================================================

import os

import mysql.connector
import pandas as pd
import streamlit as st


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DB_HOST = os.getenv(
    "MYSQL_HOST",
    "localhost"
)

DB_USER = os.getenv(
    "MYSQL_USER",
    "root"
)

DB_PASSWORD = "qwerty"

DB_NAME = os.getenv(
    "MYSQL_DATABASE",
    "cart2insights"
)


# ============================================================
# GET PASSWORD FROM STREAMLIT SECRETS
# ============================================================

if not DB_PASSWORD:

    try:
        DB_PASSWORD = st.secrets["MYSQL_PASSWORD"]

    except Exception:
        DB_PASSWORD = None


# ============================================================
# DATABASE CONNECTION
# ============================================================

@st.cache_resource
def get_connection():
    """
    Create and cache a MySQL database connection.
    """

    if not DB_PASSWORD:
        raise ValueError(
            "MYSQL_PASSWORD is not configured. "
            "Set the MYSQL_PASSWORD environment variable "
            "or add MYSQL_PASSWORD to Streamlit secrets."
        )

    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    return connection


# ============================================================
# TEST DATABASE CONNECTION
# ============================================================

def test_connection():
    """
    Test the MySQL database connection.

    Returns:
        tuple:
            (True, database_name)
            or
            (False, error_message)
    """

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            "SELECT DATABASE()"
        )

        database_name = cursor.fetchone()[0]

        cursor.close()

        return True, database_name

    except Exception as error:

        return False, str(error)


# ============================================================
# RUN SELECT QUERY
# ============================================================

def run_query(
    query,
    params=None
):
    """
    Execute a SELECT query and return
    the result as a Pandas DataFrame.

    Used by queries.py.
    """

    connection = get_connection()

    dataframe = pd.read_sql(
        query,
        connection,
        params=params
    )

    return dataframe


# ============================================================
# RUN SQL COMMAND
# ============================================================

def execute_query(
    query,
    params=None
):
    """
    Execute INSERT, UPDATE, DELETE,
    or other SQL commands.

    Returns:
        True if successful.
    """

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.execute(
            query,
            params
        )

        connection.commit()

        return True

    except Exception:

        connection.rollback()

        raise

    finally:

        cursor.close()


# ============================================================
# GET TABLE ROW COUNT
# ============================================================

def get_table_count(
    table_name
):
    """
    Return the number of rows
    in a database table.
    """

    allowed_tables = {
        "customers",
        "geolocation",
        "order_items",
        "order_payments",
        "order_reviews",
        "orders",
        "products",
        "sellers",
        "product_category_translation"
    }

    if table_name not in allowed_tables:

        raise ValueError(
            f"Invalid table name: {table_name}"
        )

    query = f"""
        SELECT COUNT(*) AS row_count
        FROM {table_name}
    """

    result = run_query(
        query
    )

    return int(
        result.loc[0, "row_count"]
    )


# ============================================================
# GET DATABASE SUMMARY
# ============================================================

def get_database_summary():
    """
    Return row counts for all project tables.
    """

    tables = [
        "customers",
        "geolocation",
        "order_items",
        "order_payments",
        "order_reviews",
        "orders",
        "products",
        "sellers",
        "product_category_translation"
    ]

    summary = []

    for table in tables:

        try:

            count = get_table_count(
                table
            )

        except Exception:

            count = None

        summary.append(
            {
                "table_name": table,
                "row_count": count
            }
        )

    return pd.DataFrame(
        summary
    )


# ============================================================
# LOAD ORDERS
# ============================================================

@st.cache_data(ttl=600)
def load_orders():
    """
    Load orders table.
    """

    query = """
        SELECT *
        FROM orders
    """

    return run_query(
        query
    )


# ============================================================
# LOAD ORDER ITEMS
# ============================================================

@st.cache_data(ttl=600)
def load_order_items():
    """
    Load order_items table.
    """

    query = """
        SELECT *
        FROM order_items
    """

    return run_query(
        query
    )


# ============================================================
# LOAD CUSTOMERS
# ============================================================

@st.cache_data(ttl=600)
def load_customers():
    """
    Load customers table.
    """

    query = """
        SELECT *
        FROM customers
    """

    return run_query(
        query
    )


# ============================================================
# LOAD SELLERS
# ============================================================

@st.cache_data(ttl=600)
def load_sellers():
    """
    Load sellers table.
    """

    query = """
        SELECT *
        FROM sellers
    """

    return run_query(
        query
    )


# ============================================================
# LOAD PRODUCTS
# ============================================================

@st.cache_data(ttl=600)
def load_products():
    """
    Load products table.
    """

    query = """
        SELECT *
        FROM products
    """

    return run_query(
        query
    )


# ============================================================
# LOAD PAYMENTS
# ============================================================

@st.cache_data(ttl=600)
def load_payments():
    """
    Load order_payments table.
    """

    query = """
        SELECT *
        FROM order_payments
    """

    return run_query(
        query
    )


# ============================================================
# LOAD REVIEWS
# ============================================================

@st.cache_data(ttl=600)
def load_reviews():
    """
    Load order_reviews table.
    """

    query = """
        SELECT *
        FROM order_reviews
    """

    return run_query(
        query
    )


# ============================================================
# LOAD GEOLOCATION
# ============================================================

@st.cache_data(ttl=600)
def load_geolocation():
    """
    Load geolocation table.
    """

    query = """
        SELECT *
        FROM geolocation
    """

    return run_query(
        query
    )


# ============================================================
# LOAD PRODUCT TRANSLATION
# ============================================================

@st.cache_data(ttl=600)
def load_translation():
    """
    Load product category translation table.
    """

    query = """
        SELECT *
        FROM product_category_translation
    """

    return run_query(
        query
    )


# ============================================================
# GET DATABASE STATUS
# ============================================================

def get_database_status():
    """
    Return database connection status.
    """

    success, result = test_connection()

    if success:

        return {
            "connected": True,
            "database": result
        }

    return {
        "connected": False,
        "database": result
    }


# ============================================================
# CLEAR STREAMLIT CACHE
# ============================================================

def clear_database_cache():
    """
    Clear cached database connection and
    cached table data.
    """

    try:
        st.cache_data.clear()

    except Exception:
        pass

    try:
        st.cache_resource.clear()

    except Exception:
        pass


# ============================================================
# TEST DATABASE MODULE
# ============================================================

if __name__ == "__main__":

    print(
        "Testing Cart2Insights database module..."
    )

    success, result = test_connection()

    if success:

        print(
            f"✅ Connected to database: {result}"
        )

        print(
            "\nDatabase Summary:"
        )

        print(
            get_database_summary()
        )

    else:

        print(
            f"❌ Database connection failed: {result}"
        )