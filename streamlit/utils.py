# ============================================================
# CART2INSIGHTS
# COMMON UTILITY FUNCTIONS
# ============================================================

import pandas as pd
import numpy as np
import streamlit as st


# ============================================================
# NUMBER FORMATTING
# ============================================================

def format_number(
    value,
    decimals=0
):
    """
    Format a numeric value with commas.
    """

    if value is None:
        return "0"

    if pd.isna(value):
        return "0"

    try:

        return f"{float(value):,.{decimals}f}"

    except (ValueError, TypeError):

        return str(value)


# ============================================================
# CURRENCY FORMATTING
# ============================================================

def format_currency(
    value,
    symbol="₹",
    decimals=2
):
    """
    Format a numeric value as currency.
    """

    if value is None:
        return f"{symbol} 0"

    if pd.isna(value):
        return f"{symbol} 0"

    try:

        return (
            f"{symbol} "
            f"{float(value):,.{decimals}f}"
        )

    except (ValueError, TypeError):

        return f"{symbol} {value}"


# ============================================================
# PERCENTAGE FORMATTING
# ============================================================

def format_percentage(
    value,
    decimals=2
):
    """
    Format a value as a percentage.
    """

    if value is None:
        return "0%"

    if pd.isna(value):
        return "0%"

    try:

        return (
            f"{float(value):.{decimals}f}%"
        )

    except (ValueError, TypeError):

        return str(value)


# ============================================================
# DECIMAL FORMATTING
# ============================================================

def format_decimal(
    value,
    decimals=2
):
    """
    Format a numeric value with decimal places.
    """

    if value is None:
        return "0.00"

    if pd.isna(value):
        return "0.00"

    try:

        return (
            f"{float(value):,.{decimals}f}"
        )

    except (ValueError, TypeError):

        return str(value)


# ============================================================
# DATE FORMATTING
# ============================================================

def format_date(
    value,
    date_format="%d %b %Y"
):
    """
    Convert a date value to a readable string.
    """

    if value is None:
        return "N/A"

    try:

        date_value = pd.to_datetime(
            value,
            errors="coerce"
        )

        if pd.isna(date_value):
            return "N/A"

        return date_value.strftime(
            date_format
        )

    except Exception:

        return "N/A"


# ============================================================
# DATAFRAME CLEANING
# ============================================================

def clean_dataframe(
    df
):
    """
    Basic cleaning for dashboard display.
    """

    if df is None:
        return pd.DataFrame()

    if not isinstance(
        df,
        pd.DataFrame
    ):
        return pd.DataFrame()

    cleaned = df.copy()

    cleaned.columns = [
        str(column)
        .strip()
        .lower()
        .replace(" ", "_")
        for column in cleaned.columns
    ]

    return cleaned


# ============================================================
# HANDLE MISSING VALUES
# ============================================================

def fill_missing_values(
    df,
    numeric_fill=0,
    text_fill="Unknown"
):
    """
    Fill missing values based on column type.
    """

    if df is None:
        return pd.DataFrame()

    result = df.copy()

    for column in result.columns:

        if pd.api.types.is_numeric_dtype(
            result[column]
        ):

            result[column] = (
                result[column]
                .fillna(numeric_fill)
            )

        else:

            result[column] = (
                result[column]
                .fillna(text_fill)
            )

    return result


# ============================================================
# SAFE DIVISION
# ============================================================

def safe_divide(
    numerator,
    denominator,
    default=0
):
    """
    Safely divide two numbers.
    """

    try:

        if denominator == 0:
            return default

        if pd.isna(denominator):
            return default

        return numerator / denominator

    except (
        ZeroDivisionError,
        TypeError,
        ValueError
    ):

        return default


# ============================================================
# CALCULATE PERCENTAGE
# ============================================================

def calculate_percentage(
    part,
    total
):
    """
    Calculate percentage safely.
    """

    return safe_divide(
        part * 100,
        total,
        default=0
    )


# ============================================================
# LIMIT TOP N
# ============================================================

def limit_top_n(
    df,
    column,
    n=10,
    ascending=False
):
    """
    Return the top N rows based on a column.
    """

    if df is None:
        return pd.DataFrame()

    if df.empty:
        return df.copy()

    if column not in df.columns:
        return df.copy()

    n = max(
        1,
        int(n)
    )

    return (
        df.sort_values(
            by=column,
            ascending=ascending
        )
        .head(n)
        .copy()
    )


# ============================================================
# CONVERT TO DATETIME
# ============================================================

def convert_to_datetime(
    df,
    columns
):
    """
    Convert selected columns to datetime.
    """

    result = df.copy()

    for column in columns:

        if column in result.columns:

            result[column] = pd.to_datetime(
                result[column],
                errors="coerce"
            )

    return result


# ============================================================
# DELIVERY STATUS
# ============================================================

def get_delivery_status(
    delivery_delay
):
    """
    Convert delivery delay into
    On Time / Delayed status.
    """

    if delivery_delay is None:
        return "Unknown"

    if pd.isna(delivery_delay):
        return "Unknown"

    try:

        if float(delivery_delay) > 0:
            return "Delayed"

        return "On Time"

    except (
        ValueError,
        TypeError
    ):

        return "Unknown"


# ============================================================
# CUSTOMER TYPE
# ============================================================

def get_customer_type(
    order_count
):
    """
    Identify one-time and repeat customers.
    """

    if order_count is None:
        return "Unknown"

    if pd.isna(order_count):
        return "Unknown"

    try:

        if int(order_count) > 1:
            return "Repeat Customer"

        return "One-time Customer"

    except (
        ValueError,
        TypeError
    ):

        return "Unknown"


# ============================================================
# REVIEW SCORE LABEL
# ============================================================

def get_review_label(
    score
):
    """
    Convert review score into a readable label.
    """

    if score is None:
        return "Unknown"

    if pd.isna(score):
        return "Unknown"

    try:

        score = float(score)

        if score >= 5:
            return "Excellent"

        if score >= 4:
            return "Good"

        if score >= 3:
            return "Average"

        if score >= 2:
            return "Poor"

        return "Very Poor"

    except (
        ValueError,
        TypeError
    ):

        return "Unknown"


# ============================================================
# RENAME COLUMNS FOR DISPLAY
# ============================================================

def prettify_columns(
    df
):
    """
    Convert database-style column names
    into readable dashboard labels.
    """

    if df is None:
        return pd.DataFrame()

    result = df.copy()

    result.columns = [
        str(column)
        .replace("_", " ")
        .title()
        for column in result.columns
    ]

    return result


# ============================================================
# CHECK DATAFRAME
# ============================================================

def is_valid_dataframe(
    df
):
    """
    Check whether a DataFrame exists
    and contains data.
    """

    return (
        isinstance(
            df,
            pd.DataFrame
        )
        and not df.empty
    )


# ============================================================
# STREAMLIT EMPTY DATA MESSAGE
# ============================================================

def show_no_data_message(
    message="No data available for the selected filters."
):
    """
    Display a consistent Streamlit message.
    """

    st.info(
        message
    )


# ============================================================
# STREAMLIT ERROR MESSAGE
# ============================================================

def show_error_message(
    message
):
    """
    Display a consistent Streamlit error.
    """

    st.error(
        message
    )


# ============================================================
# STREAMLIT SUCCESS MESSAGE
# ============================================================

def show_success_message(
    message
):
    """
    Display a consistent Streamlit success message.
    """

    st.success(
        message
    )


# ============================================================
# DISPLAY DATAFRAME
# ============================================================

def display_dataframe(
    df,
    decimals=2
):
    """
    Display a cleaned DataFrame in Streamlit.
    """

    if not is_valid_dataframe(df):

        show_no_data_message()

        return

    display_df = prettify_columns(
        clean_dataframe(df)
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# DISPLAY KPI
# ============================================================

def display_kpi(
    label,
    value,
    delta=None
):
    """
    Display a Streamlit KPI metric.
    """

    st.metric(
        label=label,
        value=value,
        delta=delta
    )


# ============================================================
# CALCULATE DELAY PERCENTAGE
# ============================================================

def calculate_delay_percentage(
    delayed_orders,
    total_orders
):
    """
    Calculate percentage of delayed orders.
    """

    return calculate_percentage(
        delayed_orders,
        total_orders
    )


# ============================================================
# CALCULATE AVERAGE ORDER VALUE
# ============================================================

def calculate_average_order_value(
    revenue,
    orders
):
    """
    Calculate average order value.
    """

    return safe_divide(
        revenue,
        orders,
        default=0
    )


# ============================================================
# CALCULATE CUSTOMER SPENDING
# ============================================================

def calculate_customer_spending(
    revenue,
    customer_count
):
    """
    Calculate average customer spending.
    """

    return safe_divide(
        revenue,
        customer_count,
        default=0
    )


# ============================================================
# PREPARE MONTHLY DATA
# ============================================================

def prepare_monthly_data(
    df,
    month_column="month"
):
    """
    Prepare monthly data for charts.
    """

    if not is_valid_dataframe(df):
        return pd.DataFrame()

    result = df.copy()

    if month_column in result.columns:

        result[month_column] = pd.to_datetime(
            result[month_column],
            errors="coerce"
        )

        result = result.sort_values(
            month_column
        )

    return result


# ============================================================
# PREPARE CHART DATA
# ============================================================

def prepare_chart_data(
    df
):
    """
    Basic preparation before sending
    data to Plotly charts.
    """

    if not is_valid_dataframe(df):
        return pd.DataFrame()

    result = df.copy()

    result = result.replace(
        [np.inf, -np.inf],
        np.nan
    )

    return result


# ============================================================
# FILTER DATAFRAME BY CATEGORY
# ============================================================

def filter_by_category(
    df,
    column,
    selected_value
):
    """
    Filter DataFrame by category.
    'All' returns the complete DataFrame.
    """

    if not is_valid_dataframe(df):
        return pd.DataFrame()

    if (
        selected_value is None
        or selected_value == "All"
    ):
        return df.copy()

    if column not in df.columns:
        return df.copy()

    return df[
        df[column] == selected_value
    ].copy()


# ============================================================
# GET UNIQUE FILTER OPTIONS
# ============================================================

def get_filter_options(
    df,
    column,
    include_all=True
):
    """
    Return unique values for Streamlit filters.
    """

    if not is_valid_dataframe(df):
        return ["All"] if include_all else []

    if column not in df.columns:
        return ["All"] if include_all else []

    values = (
        df[column]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    values = sorted(
        values
    )

    if include_all:
        return ["All"] + values

    return values


# ============================================================
# GENERATE BUSINESS INSIGHT
# ============================================================

def generate_insight(
    observation,
    interpretation,
    business_impact
):
    """
    Create a structured business insight.
    """

    return {
        "observation": observation,
        "interpretation": interpretation,
        "business_impact": business_impact
    }


# ============================================================
# DISPLAY BUSINESS INSIGHT
# ============================================================

def display_business_insight(
    observation,
    interpretation,
    business_impact
):
    """
    Display business insight using the
    project's Observation → Interpretation
    → Business Impact structure.
    """

    st.markdown(
        f"""
        **Observation:** {observation}

        **Interpretation:** {interpretation}

        **Business Impact:** {business_impact}
        """
    )


# ============================================================
# DATABASE STATUS DISPLAY
# ============================================================

def display_database_status(
    status
):
    """
    Display database connection status.
    """

    if not status:
        st.error(
            "Database status unavailable."
        )

        return

    if status.get("connected"):

        st.success(
            "🟢 Database connected: "
            f"{status.get('database', 'Unknown')}"
        )

    else:

        st.error(
            "🔴 Database connection failed: "
            f"{status.get('database', 'Unknown')}"
        )


# ============================================================
# SIDEBAR FILTER VALIDATION
# ============================================================

def validate_date_range(
    start_date,
    end_date
):
    """
    Validate dashboard date range.
    """

    if start_date is None:
        return False

    if end_date is None:
        return False

    if start_date > end_date:
        return False

    return True


# ============================================================
# PROJECT INFORMATION
# ============================================================

def get_project_info():

    return {
        "name": "Cart2Insights",
        "title": "Decoding E-Commerce Performance",
        "database": "cart2insights",
        "dashboard": "Streamlit",
        "database_engine": "MySQL"
    }


# ============================================================
# TEST UTILITIES
# ============================================================

if __name__ == "__main__":

    print(
        "Cart2Insights utils.py"
    )

    print(
        "Currency:",
        format_currency(123456.78)
    )

    print(
        "Number:",
        format_number(123456.78, 2)
    )

    print(
        "Percentage:",
        format_percentage(82.4567)
    )

    print(
        "Delivery status:",
        get_delivery_status(3)
    )

    print(
        "Customer type:",
        get_customer_type(3)
    )

    print(
        "Review label:",
        get_review_label(5)
    )

    print(
        "Average order value:",
        calculate_average_order_value(
            10000,
            100
        )
    )

    print(
        "Delay percentage:",
        calculate_delay_percentage(
            20,
            100
        )
    )

    print(
        "Project info:",
        get_project_info()
    )

    print(
        "✅ utils.py test completed successfully"
    )