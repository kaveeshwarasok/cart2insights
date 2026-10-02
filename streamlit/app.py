# ============================================================
# CART2INSIGHTS
# E-COMMERCE PERFORMANCE DASHBOARD  (modern UI)
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from database import (
    get_database_status,
    get_database_summary
)

from queries import (
    get_business_overview,
    get_monthly_revenue,
    get_revenue_by_category,
    get_top_products,
    get_sales_by_location,
    get_customer_distribution,
    get_repeat_customers,
    get_top_customers,
    get_seller_performance,
    get_top_sellers,
    get_category_performance,
    get_seller_ranking,
    get_category_ranking,
    get_delivery_performance,
    get_delivery_by_location,
    get_delivery_review_analysis,
    get_review_score_distribution,
    get_reviews_by_category,
    get_payment_method_analysis,
    get_payment_order_status,
    get_order_status_analysis,
    get_average_order_value,
    get_customer_spending_segments,
    get_monthly_customer_growth,
    get_monthly_delivery_performance,
)

from utils import (
    format_number,
    format_currency,
    format_decimal,
    format_percentage,
    display_dataframe,
    display_business_insight,
    display_database_status,
    prepare_monthly_data,
    prepare_chart_data,
    is_valid_dataframe,
    show_no_data_message,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Cart2Insights",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DESIGN TOKENS
# ============================================================

INK = "#F5F7FA"          # sidebar / headings
INK_SOFT = "#9AA4B2"     # secondary text

CANVAS = "#0E1117"       # page background

TEAL = "#2DD4BF"         # primary chart color
AMBER = "#F2C14E"        # active / highlight
CORAL = "#F06C5B"        # negative / delayed
INDIGO = "#818CF8"       # secondary chart color

PALETTE = [
    TEAL,
    INDIGO,
    AMBER,
    CORAL,
    "#94A3B8",            # slate
    "#38BDF8",            # sky blue
    "#C084FC",            # soft purple
    "#A3E635"             # lime
]

px.defaults.template = "plotly_dark"
px.defaults.color_discrete_sequence = PALETTE

px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = PALETTE


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stApp {{
        font-family: 'Manrope', sans-serif;
    }}

    .stApp {{
        background: {CANVAS};
    }}

   /* hide default chrome */
#MainMenu,
footer {{
    visibility: hidden;
    height: 0;
}}

/* Keep sidebar toggle button visible */
header[data-testid="stHeader"] {{
    background: transparent;
}}

button[data-testid="stSidebarCollapseButton"] {{
    visibility: visible !important;
    display: flex !important;
    opacity: 1 !important;
    color: {INK} !important;
}}
    .block-container {{
        padding-top: 1.6rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }}

    h1, h2, h3, h4 {{
        color: {INK};
        font-weight: 700;
        letter-spacing: -0.01em;
    }}

    /* ---------- SIDEBAR ---------- */
    section[data-testid="stSidebar"] {{
        background:{CANVAS} ;
        border-right: 3px solid white;
    }}

    section[data-testid="stSidebar"] > div {{
        padding-top: 1rem;
    }}

    section[data-testid="stSidebar"] * {{
        color: #d7deec;
    }}

    .brand {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 6px 4px 4px 4px;
    }}

    .brand-logo {{
        width: 42px;
        height: 42px;
        border:1px solid white;
        padding:30px;
        border-radius: 12px;
        background: #0E11176E;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
    }}

    .brand-name {{
        font-size: 20px;
        font-weight: 800;
        color: #ffffff !important;
        line-height: 1.1;
    }}

    .brand-tag {{
        font-size: 12px;
        color: #8d9bb8 !important;
    }}

    .nav-label {{
        font-size: 12px;
        font-weight: 600;
        color: #7f8db0 !important;
        margin: 18px 0 6px 6px;
    }}

    section[data-testid="stSidebar"] hr {{
        border-color: rgba(255, 255, 255, 0.08);
        margin: 14px 0;
    }}

    /* radio -> nav menu */
    section[data-testid="stSidebar"] div[role="radiogroup"] {{
        gap: 4px;
    }}

    section[data-testid="stSidebar"] div[role="radiogroup"] label {{
        width: 100%;
        padding: 10px 14px;
        border-radius: 10px;
        cursor: pointer;
        transition: background 0.15s ease;
        border: 1px solid transparent;
    }}

    section[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {{
        display: none;
    }}

    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
        background: rgba(255, 255, 255, 0.07);
    }}

    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {{
        background: rgba(245, 165, 36, 0.16);
        border: 1px solid rgba(245, 165, 36, 0.45);
    }}

    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {{
        color: {AMBER} !important;
        font-weight: 700;
    }}

    section[data-testid="stSidebar"] div[role="radiogroup"] label p {{
        font-size: 15px;
        font-weight: 500;
    }}

    section[data-testid="stSidebar"] .stButton button {{
        width: 100%;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.14);
        color: #ffffff;
    }}

    section[data-testid="stSidebar"] .stButton button:hover {{
        border-color: {AMBER};
        color: {AMBER};
    }}

    /* ---------- HERO ---------- */
    .hero {{
        background: linear-gradient(120deg, #1f3a6b 60%, {TEAL} 135%);
        border-radius: 18px;
        padding: 28px 32px;
        margin-bottom: 70px;
        box-shadow: 0 10px 30px rgba(19, 32, 58, 0.18);
    }}

    .hero h1 {{
        color: #ffffff;
        font-size: 30px;
        margin: 0 0 6px 0;
        padding: 0;
    }}

    .hero p {{
        color: #c5d0e6;
        font-size: 15px;
        margin: 0;
        max-width: 760px;
    }}

    /* ---------- SECTION HEADER ---------- */
    .sec-head {{
        display: flex;
        align-items: center;
        gap: 14px;
        margin: 4px 0 18px 0;
    }}

    .sec-icon {{
        width: 46px;
        height: 46px;
        border-radius: 13px;
        background: #ffffff;
        border: 1px solid #e3e8f0;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
    }}

    .sec-title {{
        font-size: 24px;
        font-weight: 800;
        color: {INK};
        line-height: 1.15;
    }}

    .sec-desc {{
        font-size: 14px;
        color: {INK_SOFT};
    }}

    .sub-title {{
        font-size: 17px;
        font-weight: 700;
        color: {INK};
        margin: 26px 0 10px 2px;
    }}

    /* ---------- KPI CARD ---------- */
    .kpi {{
        background: #0E11176E;
        border: 0.5px solid #e3e8f0;
        border-left: 2.5px solid var(--accent, {TEAL});
        border-radius: 14px;
        padding: 5px 10px;
        margin-bottom: 14px;
        box-shadow: 0 2px 8px rgba(19, 32, 58, 0.04);
    }}

    .kpi-top {{
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    .kpi-label {{
        font-size: 13px;
        font-weight: 600;
        color: {INK_SOFT};
    }}

    .kpi-icon {{
        font-size: 18px;
    }}

    .kpi-value {{
        font-size: 30px;
        font-weight: 800;
        color: {INK};
        margin-top: 6px;
        letter-spacing: -0.02em;
    }}

    /* ---------- CONTAINERS / CHART CARDS ---------- */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > div[data-testid="stVerticalBlock"] .js-plotly-plot),
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        border-radius: 14px;
    }}

    div[data-testid="stVerticalBlockBorderWrapper"] > div[style*="border"],
    div[data-testid="stVerticalBlockBorderWrapper"][class*="st-"] {{
        background: #ffffff;
    }}

    div[data-testid="stExpander"] {{
        background: #0E11176E;
        border: 1px solid #e3e8f0;
        border-radius: 12px;
    }}

    /* ---------- TABS ---------- */
    button[data-baseweb="tab"] {{
        font-weight: 600;
        font-size: 15px;
    }}

    div[data-baseweb="tab-highlight"] {{
        background-color: {TEAL};
    }}

    /* ---------- INSIGHT CARD ---------- */
    .insight-card {{
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #e3e8f0;
        border-left: 5px solid {AMBER};
        background-color: #ffffff;
        margin-bottom: 10px;
    }}

    /* ---------- FOOTER ---------- */
    .app-footer {{
        text-align: center;
        color: {INK_SOFT};
        font-size: 13px;
        padding: 18px 0 4px 0;
    }}

    
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    f"""
    <style>

    /* ---------- HIDE SIDEBAR SCROLLBAR ---------- */
    section[data-testid="stSidebar"] > div {{
        padding-top: 1rem;
        scrollbar-width: none;
        -ms-overflow-style: none;
    }}

    section[data-testid="stSidebar"] > div::-webkit-scrollbar {{
        display: none;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DASHBOARD HELPERS
# ============================================================

def hero(title, subtitle):
    """Top banner shown on every page."""

    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_header(title, description=None, icon="📊"):
    """Display a dashboard section heading with an icon tile."""

    st.markdown(
        f"""
        <div class="sec-head">
            <div class="sec-icon">{icon}</div>
            <div>
                <div class="sec-title">{title}</div>
                <div class="sec-desc">{description or ""}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def sub_title(text):
    """Heading for a block inside a section."""

    st.markdown(
        f'<div class="sub-title">{text}</div>',
        unsafe_allow_html=True
    )


def kpi_card(label, value, icon="📈", accent=TEAL):
    """Modern KPI card."""

    st.markdown(
        f"""
        <div class="kpi" style="--accent:{accent};">
            <div class="kpi-top">
                <span class="kpi-label">{label}</span>
                <span class="kpi-icon">{icon}</span>
            </div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def safe_numeric(df, columns):
    """Convert selected DataFrame columns to numeric safely."""

    if df is None or df.empty:

        return df

    result = df.copy()

    for column in columns:

        if column in result.columns:

            result[column] = pd.to_numeric(
                result[column],
                errors="coerce"
            )

    return result


def shorten_ids(df, column, length=8):
    """Shorten long hash IDs so chart labels stay readable."""

    result = df.copy()

    result[column] = (
        result[column]
        .astype(str)
        .str.slice(0, length) + "…"
    )

    return result


def style_fig(fig, height=400, legend=False):
    """Apply the shared chart look."""

    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Manrope, sans-serif", color=INK, size=13),
        title=dict(font=dict(size=16, color=INK), x=0.01),
        showlegend=legend,
        hoverlabel=dict(font_family="Manrope, sans-serif"),
    )

    fig.update_xaxes(showgrid=False, linecolor="#d9dfeb")
    fig.update_yaxes(gridcolor="#edf0f6", zeroline=False)

    return fig


def show_chart(fig, height=400, legend=False):
    """Render a chart inside a bordered card."""

    with st.container(border=True):

        st.plotly_chart(
            style_fig(fig, height, legend),
            use_container_width=True,
            config={"displayModeBar": False}
        )


def data_table(df, label="View data"):
    """Collapsible data table."""

    with st.expander(label):

        display_dataframe(df)


def hbar(df, x, y, title, color=None, height=420):
    """Horizontal ranking bar chart."""

    fig = px.bar(
        df,
        x=x,
        y=y,
        orientation="h",
        color=color,
        title=title
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    fig.update_traces(marker_line_width=0)

    show_chart(fig, height, legend=color is not None)


# ============================================================
# DATABASE STATUS
# ============================================================

db_status = get_database_status()

SECTIONS = {
    "Business Overview": ("📊", "Business Overview"),
    "Sales Analysis": ("💰", "Sales Analysis"),
    "Customer Analysis": ("👥", "Customer Analysis"),
    "Seller & Product Analysis": ("🏪", "Seller & Product Analysis"),
    "Delivery Analysis": ("🚚", "Delivery Analysis"),
    "Customer Experience": ("⭐", "Customer Experience"),
    "SQL Analysis": ("🧮", "SQL Analysis"),
    "Database Status": ("🗄️", "Database Status"),
}


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <div class="brand-logo">🛒</div>
            <div>
                <div class="brand-name">Cart2Insights</div>
                <div class="brand-tag"> </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    if not db_status.get("connected"):

        display_database_status(db_status)

        st.stop()

    st.markdown(
        '<div class="nav-label">Navigate</div>',
        unsafe_allow_html=True
    )

    selected_section = st.radio(
        "Go to",
        list(SECTIONS.keys()),
        format_func=lambda name: f"{SECTIONS[name][0]}  {name}",
        label_visibility="collapsed"
    )

    st.divider()

    if st.button("🔄  Refresh data"):

        st.cache_data.clear()
        st.rerun()

    with st.expander("Connection"):

        display_database_status(db_status)

    st.markdown(
        """
        <div class="nav-label">Built with</div>
        <div style="font-size:13px; line-height:1.9;">
            MySQL · Python · Pandas<br>Plotly · Streamlit
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# LOAD DASHBOARD DATA
# ============================================================

@st.cache_data(ttl=600)
def load_dashboard_data():

    return {

        "overview": get_business_overview(),
        "monthly_revenue": get_monthly_revenue(),
        "revenue_category": get_revenue_by_category(),
        "top_products": get_top_products(10),
        "sales_location": get_sales_by_location(),
        "customer_distribution": get_customer_distribution(),
        "repeat_customers": get_repeat_customers(),
        "top_customers": get_top_customers(10),
        "seller_performance": get_seller_performance(),
        "top_sellers": get_top_sellers(10),
        "category_performance": get_category_performance(),
        "seller_ranking": get_seller_ranking(),
        "category_ranking": get_category_ranking(),
        "delivery": get_delivery_performance(),
        "delivery_location": get_delivery_by_location(),
        "delivery_review": get_delivery_review_analysis(),
        "review_distribution": get_review_score_distribution(),
        "reviews_category": get_reviews_by_category(),
        "payment_methods": get_payment_method_analysis(),
        "payment_status": get_payment_order_status(),
        "order_status": get_order_status_analysis(),
        "average_order_value": get_average_order_value(),
        "customer_segments": get_customer_spending_segments(),
        "customer_growth": get_monthly_customer_growth(),
        "monthly_delivery": get_monthly_delivery_performance(),
    }


try:

    with st.spinner("Loading dashboard data…"):

        data = load_dashboard_data()

except Exception as error:

    st.error("Unable to load dashboard data.")

    st.exception(error)

    st.stop()


# ============================================================
# HERO
# ============================================================

hero(
    "Cart2Insights",
    "Sales, customers, sellers, delivery, payments and reviews "
    "from the Olist e-commerce dataset, in one place."
)


# ============================================================
# 1. BUSINESS OVERVIEW
# ============================================================

if selected_section == "Business Overview":

    section_header(
        "Business Overview",
        "High-level business performance indicators.",
        "📊"
    )

    overview = data["overview"]

    if not is_valid_dataframe(overview):

        show_no_data_message("No business overview data available.")

    else:

        overview = overview.iloc[0]

        c1, c2, c3 = st.columns(3)

        with c1:
            kpi_card(
                "Total Revenue",
                format_currency(overview["total_revenue"]),
                "💰", TEAL
            )

        with c2:
            kpi_card(
                "Total Orders",
                format_number(overview["total_orders"]),
                "📦", INDIGO
            )

        with c3:
            kpi_card(
                "Average Order Value",
                format_currency(overview["average_order_value"]),
                "🧾", AMBER
            )

        c4, c5, c6 = st.columns(3)

        with c4:
            kpi_card(
                "Total Customers",
                format_number(overview["total_customers"]),
                "👥", INDIGO
            )

        with c5:
            kpi_card(
                "Total Sellers",
                format_number(overview["total_sellers"]),
                "🏪", TEAL
            )

        with c6:
            kpi_card(
                "Average Review Score",
                format_decimal(overview["average_review_score"], 2),
                "⭐", AMBER
            )

    # quick trend preview
    monthly_preview = data["monthly_revenue"].copy()

    if is_valid_dataframe(monthly_preview):

        monthly_preview = safe_numeric(monthly_preview, ["revenue"])

        monthly_preview = prepare_monthly_data(monthly_preview, "month")

        fig = px.area(
            monthly_preview,
            x="month",
            y="revenue",
            title="Revenue over time"
        )

        fig.update_traces(
            line_color=TEAL,
            fillcolor="rgba(15, 157, 138, 0.15)"
        )

        fig.update_layout(
            xaxis_title=None,
            yaxis_title="Revenue",
            hovermode="x unified"
        )

        show_chart(fig, 340)

    sub_title("Business insights")

    display_business_insight(
        "Revenue is calculated from product price and freight value.",
        "Both product value and shipping contribution are included in revenue.",
        "This provides a broader view of the monetary value generated by orders."
    )

    display_business_insight(
        "Customer experience is represented by review scores.",
        "Review scores provide a customer feedback indicator.",
        "Delivery and product performance can be investigated alongside customer satisfaction."
    )


# ============================================================
# 2. SALES ANALYSIS
# ============================================================

elif selected_section == "Sales Analysis":

    section_header(
        "Sales Analysis",
        "Revenue trends, product categories, products and geographic sales.",
        "💰"
    )

    # ---------------- monthly revenue ----------------

    monthly = data["monthly_revenue"].copy()

    if is_valid_dataframe(monthly):

        monthly = safe_numeric(monthly, ["revenue", "orders", "customers"])

        monthly = prepare_monthly_data(monthly, "month")

        fig = px.line(
            monthly,
            x="month",
            y="revenue",
            markers=True,
            title="Monthly revenue trend"
        )

        fig.update_traces(line_color=TEAL, line_width=3)

        fig.update_layout(
            xaxis_title=None,
            yaxis_title="Revenue",
            hovermode="x unified"
        )

        show_chart(fig, 380)

    else:

        show_no_data_message("No monthly revenue data available.")

    # ---------------- category + location ----------------

    left, right = st.columns(2)

    with left:

        category = data["revenue_category"].copy()

        if is_valid_dataframe(category):

            category = safe_numeric(category, ["revenue"])

            category = prepare_chart_data(category)

            hbar(
                category.head(15),
                "revenue",
                "category",
                "Top categories by revenue",
                height=480
            )

    with right:

        location = data["sales_location"].copy()

        if is_valid_dataframe(location):

            location = safe_numeric(
                location,
                ["orders", "customers", "revenue", "average_item_value"]
            )

            fig = px.bar(
                location.head(15),
                x="state",
                y="revenue",
                title="Revenue by customer state"
            )

            fig.update_traces(marker_color=INDIGO)

            fig.update_layout(xaxis_title=None)

            show_chart(fig, 480)

    if is_valid_dataframe(data["sales_location"]):

        data_table(location, "View sales by location")

    # ---------------- top products ----------------

    sub_title("Top-selling products")

    products = data["top_products"].copy()

    if is_valid_dataframe(products):

        products = safe_numeric(
            products,
            ["revenue", "freight_revenue", "units_sold", "orders"]
        )

        products_chart = shorten_ids(products, "product_id")

        hbar(
            products_chart,
            "revenue",
            "product_id",
            "Top 10 products by revenue",
            color="category",
            height=440
        )

        data_table(products, "View product data")


# ============================================================
# 3. CUSTOMER ANALYSIS
# ============================================================

elif selected_section == "Customer Analysis":

    section_header(
        "Customer Analysis",
        "Customer distribution, spending, repeat behavior and customer value.",
        "👥"
    )

    left, right = st.columns([3, 2])

    # ---------------- distribution ----------------

    with left:

        customer_distribution = data["customer_distribution"].copy()

        if is_valid_dataframe(customer_distribution):

            customer_distribution = safe_numeric(
                customer_distribution,
                ["customers", "orders", "spending"]
            )

            fig = px.bar(
                customer_distribution.head(15),
                x="state",
                y="customers",
                title="Customers by state"
            )

            fig.update_traces(marker_color=TEAL)

            fig.update_layout(xaxis_title=None)

            show_chart(fig, 380)

    # ---------------- repeat vs one-time ----------------

    with right:

        repeat = data["repeat_customers"].copy()

        if is_valid_dataframe(repeat):

            repeat = safe_numeric(repeat, ["customers"])

            fig = px.pie(
                repeat,
                names="customer_type",
                values="customers",
                hole=0.55,
                title="Repeat vs one-time customers"
            )

            fig.update_traces(textinfo="percent")

            show_chart(fig, 380, legend=True)

    if is_valid_dataframe(data["customer_distribution"]):

        data_table(customer_distribution, "View customer distribution")

    if is_valid_dataframe(data["repeat_customers"]):

        data_table(repeat, "View repeat customer data")

    # ---------------- segments + growth ----------------

    left, right = st.columns(2)

    with left:

        segments = data["customer_segments"].copy()

        if is_valid_dataframe(segments):

            segments = safe_numeric(
                segments,
                ["customers", "average_spending"]
            )

            fig = px.bar(
                segments,
                x="spending_segment",
                y="customers",
                title="Customers by spending segment"
            )

            fig.update_traces(marker_color=AMBER)

            fig.update_layout(xaxis_title=None)

            show_chart(fig, 360)

    with right:

        growth = data["customer_growth"].copy()

        if is_valid_dataframe(growth):

            growth = safe_numeric(growth, ["active_customers", "orders"])

            growth = prepare_monthly_data(growth, "month")

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=growth["month"],
                    y=growth["active_customers"],
                    mode="lines+markers",
                    name="Active customers",
                    line=dict(color=INDIGO, width=3)
                )
            )

            fig.update_layout(
                title="Monthly active customers",
                yaxis_title="Customers"
            )

            show_chart(fig, 360)

    if is_valid_dataframe(data["customer_segments"]):

        data_table(segments, "View spending segments")

    # ---------------- top customers ----------------

    sub_title("Top customers by spending")

    top_customers = data["top_customers"].copy()

    if is_valid_dataframe(top_customers):

        top_customers = safe_numeric(
            top_customers,
            ["order_count", "total_spending", "average_order_value"]
        )

        hbar(
            shorten_ids(top_customers, "customer_unique_id"),
            "total_spending",
            "customer_unique_id",
            "Top 10 customers by spending",
            height=420
        )

        data_table(top_customers, "View top customer data")


# ============================================================
# 4. SELLER & PRODUCT ANALYSIS
# ============================================================

elif selected_section == "Seller & Product Analysis":

    section_header(
        "Seller & Product Analysis",
        "Seller performance, product categories and revenue rankings.",
        "🏪"
    )

    left, right = st.columns(2)

    # ---------------- top sellers ----------------

    with left:

        sellers = data["top_sellers"].copy()

        if is_valid_dataframe(sellers):

            sellers = safe_numeric(
                sellers,
                ["order_count", "items_sold", "seller_revenue"]
            )

            hbar(
                shorten_ids(sellers, "seller_id"),
                "seller_revenue",
                "seller_id",
                "Top 10 sellers by revenue",
                height=440
            )

    # ---------------- category performance ----------------

    with right:

        category_performance = data["category_performance"].copy()

        if is_valid_dataframe(category_performance):

            category_performance = safe_numeric(
                category_performance,
                ["products", "units_sold", "revenue", "average_price"]
            )

            hbar(
                category_performance.head(15),
                "revenue",
                "category",
                "Category revenue performance",
                height=440
            )

    if is_valid_dataframe(data["top_sellers"]):

        data_table(sellers, "View top seller data")

    # ---------------- tables ----------------

    tab_perf, tab_seller, tab_cat = st.tabs(
        ["Seller performance", "Seller ranking", "Category ranking"]
    )

    with tab_perf:

        seller_performance = data["seller_performance"].copy()

        if is_valid_dataframe(seller_performance):

            seller_performance = safe_numeric(
                seller_performance,
                ["order_count", "items_sold", "seller_revenue", "average_item_price"]
            )

            display_dataframe(seller_performance.head(20))

    with tab_seller:

        seller_ranking = data["seller_ranking"].copy()

        if is_valid_dataframe(seller_ranking):

            seller_ranking = safe_numeric(
                seller_ranking,
                ["revenue", "revenue_rank"]
            )

            display_dataframe(seller_ranking.head(20))

    with tab_cat:

        category_ranking = data["category_ranking"].copy()

        if is_valid_dataframe(category_ranking):

            category_ranking = safe_numeric(
                category_ranking,
                ["revenue", "revenue_rank"]
            )

            display_dataframe(category_ranking.head(20))


# ============================================================
# 5. DELIVERY ANALYSIS
# ============================================================

elif selected_section == "Delivery Analysis":

    section_header(
        "Delivery Analysis",
        "Delivery speed, delays, geographic performance and customer impact.",
        "🚚"
    )

    left, right = st.columns([2, 3])

    # ---------------- on-time vs delayed ----------------

    with left:

        delivery = data["delivery"].copy()

        if is_valid_dataframe(delivery):

            delivery = safe_numeric(
                delivery,
                ["orders", "average_delivery_days"]
            )

            fig = px.pie(
                delivery,
                names="delivery_status",
                values="orders",
                hole=0.55,
                title="On-time vs delayed orders"
            )

            fig.update_traces(textinfo="percent")

            show_chart(fig, 380, legend=True)

    # ---------------- delivery by state ----------------

    with right:

        delivery_location = data["delivery_location"].copy()

        if is_valid_dataframe(delivery_location):

            delivery_location = safe_numeric(
                delivery_location,
                ["orders", "average_delivery_days", "average_delay_days"]
            )

            fig = px.bar(
                delivery_location.head(15),
                x="state",
                y="average_delivery_days",
                title="Average delivery days by state"
            )

            fig.update_traces(marker_color=INDIGO)

            fig.update_layout(xaxis_title=None)

            show_chart(fig, 380)

    if is_valid_dataframe(data["delivery"]):

        data_table(delivery, "View delivery status data")

    if is_valid_dataframe(data["delivery_location"]):

        data_table(delivery_location, "View delivery location data")

    # ---------------- monthly delivery ----------------

    sub_title("Monthly delivery performance")

    monthly_delivery = data["monthly_delivery"].copy()

    if is_valid_dataframe(monthly_delivery):

        monthly_delivery = safe_numeric(
            monthly_delivery,
            ["average_delivery_days", "delayed_percentage"]
        )

        monthly_delivery = prepare_monthly_data(monthly_delivery, "month")

        fig = px.line(
            monthly_delivery,
            x="month",
            y="delayed_percentage",
            markers=True,
            title="Monthly delayed order percentage"
        )

        fig.update_traces(line_color=CORAL, line_width=3)

        fig.update_layout(
            xaxis_title=None,
            yaxis_title="Delayed orders (%)",
            hovermode="x unified"
        )

        show_chart(fig, 360)


# ============================================================
# 6. CUSTOMER EXPERIENCE
# ============================================================

elif selected_section == "Customer Experience":

    section_header(
        "Customer Experience",
        "Reviews and the relationship between delivery and satisfaction.",
        "⭐"
    )

    left, right = st.columns(2)

    # ---------------- review distribution ----------------

    with left:

        reviews = data["review_distribution"].copy()

        if is_valid_dataframe(reviews):

            reviews = safe_numeric(
                reviews,
                ["review_score", "review_count", "percentage"]
            )

            fig = px.bar(
                reviews,
                x="review_score",
                y="review_count",
                text="percentage",
                title="Review score distribution"
            )

            fig.update_traces(marker_color=AMBER, textposition="outside")

            fig.update_layout(
                xaxis_title="Review score",
                yaxis_title="Number of reviews"
            )

            show_chart(fig, 380)

    # ---------------- delivery vs review ----------------

    with right:

        delivery_review = data["delivery_review"].copy()

        if is_valid_dataframe(delivery_review):

            delivery_review = safe_numeric(
                delivery_review,
                ["average_review_score", "review_count"]
            )

            fig = px.bar(
                delivery_review,
                x="delivery_status",
                y="average_review_score",
                text="average_review_score",
                title="Average review score by delivery status"
            )

            fig.update_traces(marker_color=TEAL, textposition="outside")

            fig.update_layout(xaxis_title=None)

            show_chart(fig, 380)

    if is_valid_dataframe(data["review_distribution"]):

        data_table(reviews, "View review distribution")

    if is_valid_dataframe(data["delivery_review"]):

        data_table(delivery_review, "View delivery vs review data")

    # ---------------- reviews by category ----------------

    sub_title("Reviews by product category")

    reviews_category = data["reviews_category"].copy()

    if is_valid_dataframe(reviews_category):

        reviews_category = safe_numeric(
            reviews_category,
            ["reviews", "average_review_score"]
        )

        hbar(
            reviews_category.head(15),
            "average_review_score",
            "category",
            "Average review score by category",
            height=480
        )


# ============================================================
# 7. SQL ANALYSIS
# ============================================================

elif selected_section == "SQL Analysis":

    section_header(
        "SQL Analysis",
        "Business analysis generated directly from MySQL using SQL queries.",
        "🧮"
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Order status", "Payment analysis", "AOV analysis", "Rankings"]
    )

    # ---------------- order status ----------------

    with tab1:

        order_status = data["order_status"].copy()

        if is_valid_dataframe(order_status):

            order_status = safe_numeric(
                order_status,
                ["orders", "percentage"]
            )

            fig = px.pie(
                order_status,
                names="order_status",
                values="orders",
                hole=0.5,
                title="Orders by status"
            )

            show_chart(fig, 420, legend=True)

            data_table(order_status, "View order status data")

    # ---------------- payments ----------------

    with tab2:

        left, right = st.columns(2)

        with left:

            payment_methods = data["payment_methods"].copy()

            if is_valid_dataframe(payment_methods):

                payment_methods = safe_numeric(
                    payment_methods,
                    ["orders", "payment_value", "average_payment_value"]
                )

                fig = px.bar(
                    payment_methods,
                    x="payment_type",
                    y="payment_value",
                    title="Payment value by method"
                )

                fig.update_traces(marker_color=TEAL)

                fig.update_layout(xaxis_title=None)

                show_chart(fig, 380)

        with right:

            payment_status = data["payment_status"].copy()

            if is_valid_dataframe(payment_status):

                payment_status = safe_numeric(payment_status, ["orders"])

                fig = px.bar(
                    payment_status,
                    x="payment_type",
                    y="orders",
                    color="order_status",
                    barmode="group",
                    title="Payment method vs order status"
                )

                fig.update_layout(xaxis_title=None)

                show_chart(fig, 380, legend=True)

        if is_valid_dataframe(data["payment_methods"]):

            data_table(payment_methods, "View payment method data")

        if is_valid_dataframe(data["payment_status"]):

            data_table(payment_status, "View payment status data")

    # ---------------- AOV ----------------

    with tab3:

        aov = data["average_order_value"].copy()

        if is_valid_dataframe(aov):

            row = aov.iloc[0]

            c1, c2, c3 = st.columns(3)

            with c1:
                kpi_card(
                    "Average order value",
                    format_currency(row["average_order_value"]),
                    "🧾", TEAL
                )

            with c2:
                kpi_card(
                    "Minimum order value",
                    format_currency(row["minimum_order_value"]),
                    "⬇️", INDIGO
                )

            with c3:
                kpi_card(
                    "Maximum order value",
                    format_currency(row["maximum_order_value"]),
                    "⬆️", AMBER
                )

            data_table(aov, "View AOV data")

        sub_title("Customer spending segments")

        display_dataframe(data["customer_segments"])

    # ---------------- rankings ----------------

    with tab4:

        sub_title("Seller revenue ranking")

        display_dataframe(data["seller_ranking"].head(20))

        sub_title("Category revenue ranking")

        display_dataframe(data["category_ranking"].head(20))


# ============================================================
# 8. DATABASE STATUS
# ============================================================

elif selected_section == "Database Status":

    section_header(
        "Database Status",
        "Check the MySQL connection and table row counts.",
        "🗄️"
    )

    display_database_status(get_database_status())

    try:

        summary = get_database_summary()

        if is_valid_dataframe(summary):

            summary = summary.copy()

            summary["row_count"] = pd.to_numeric(
                summary["row_count"],
                errors="coerce"
            )

            total_rows = summary["row_count"].sum()

            c1, c2 = st.columns(2)

            with c1:
                kpi_card(
                    "Total database rows",
                    format_number(total_rows),
                    "🗄️", TEAL
                )

            with c2:
                kpi_card(
                    "Tables",
                    format_number(len(summary)),
                    "📋", INDIGO
                )

            sub_title("Database tables")

            display_dataframe(summary)

        else:

            show_no_data_message("No database table information available.")

    except Exception as error:

        st.error("Unable to load database summary.")

        st.exception(error)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="app-footer">'
    "Cart2Insights · E-commerce performance analytics · "
    "MySQL, Python, Pandas, Plotly, Streamlit"
    "</div>",
    unsafe_allow_html=True
)