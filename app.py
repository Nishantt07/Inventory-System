import pandas as pd
import plotly.express as px
import streamlit as st

from inventory_reconciliation import build_reconciliation, load_data


st.set_page_config(
    page_title="Divine Hindu Inventory Dashboard",
    page_icon="DH",
    layout="wide",
)


@st.cache_data
def get_reconciliation_data():
    return build_reconciliation()


@st.cache_data
def get_raw_data():
    return load_data()


report = get_reconciliation_data()
sku_master, stock_movements, physical_count = get_raw_data()

st.title("Divine Hindu - Bangalore Inventory Dashboard")
st.caption(
    "Practical inventory tracking system for SKU-wise stock, sales, returns, damage, "
    "low-stock alerts, and physical stock reconciliation."
)

with st.sidebar:
    st.header("Filters")

    categories = ["All"] + sorted(report["category"].unique().tolist())
    selected_category = st.selectbox("Category", categories)

    statuses = ["All", "Healthy", "Low Stock"]
    selected_stock_status = st.selectbox("Stock Status", statuses)

    mismatch_statuses = ["All", "Matched", "Mismatch"]
    selected_mismatch_status = st.selectbox("Mismatch Status", mismatch_statuses)

filtered = report.copy()

if selected_category != "All":
    filtered = filtered[filtered["category"] == selected_category]

if selected_stock_status != "All":
    filtered = filtered[filtered["low_stock_status"] == selected_stock_status]

if selected_mismatch_status != "All":
    filtered = filtered[filtered["mismatch_status"] == selected_mismatch_status]


total_skus = report["sku"].nunique()
total_units = int(report["calculated_closing_stock"].sum())
low_stock_count = int((report["low_stock_status"] == "Low Stock").sum())
mismatch_count = int((report["mismatch_status"] == "Mismatch").sum())
damaged_units = int(report["damaged_stock"].sum())
stock_value = int(report["stock_value_at_cost"].sum())

kpi_1, kpi_2, kpi_3, kpi_4, kpi_5 = st.columns(5)

kpi_1.metric("Total SKUs", total_skus)
kpi_2.metric("Closing Units", total_units)
kpi_3.metric("Low Stock Items", low_stock_count)
kpi_4.metric("Mismatch Items", mismatch_count)
kpi_5.metric("Stock Value", f"Rs. {stock_value:,}")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Category-wise Closing Stock")
    category_stock = (
        report.groupby("category", as_index=False)["calculated_closing_stock"]
        .sum()
        .sort_values("calculated_closing_stock", ascending=False)
    )

    fig_category = px.bar(
        category_stock,
        x="category",
        y="calculated_closing_stock",
        text="calculated_closing_stock",
        title=None,
    )
    fig_category.update_layout(
        xaxis_title="Category",
        yaxis_title="Closing Stock",
        height=380,
    )
    st.plotly_chart(fig_category, use_container_width=True)

with right:
    st.subheader("Stock Health Summary")
    health_summary = (
        report["low_stock_status"]
        .value_counts()
        .reset_index()
    )
    health_summary.columns = ["status", "count"]

    fig_health = px.pie(
        health_summary,
        names="status",
        values="count",
        hole=0.45,
    )
    fig_health.update_layout(height=380)
    st.plotly_chart(fig_health, use_container_width=True)

st.divider()

st.subheader("Low Stock Alerts")

low_stock_table = report[report["low_stock_status"] == "Low Stock"][
    [
        "sku",
        "product_name",
        "category",
        "calculated_closing_stock",
        "min_stock",
        "reorder_recommendation",
        "supplier",
    ]
]

if low_stock_table.empty:
    st.success("No low-stock items currently.")
else:
    st.warning("These SKUs need reorder attention.")
    st.dataframe(low_stock_table, use_container_width=True, hide_index=True)

st.subheader("Mismatch Report")

mismatch_table = report[report["mismatch_status"] == "Mismatch"][
    [
        "sku",
        "product_name",
        "category",
        "calculated_closing_stock",
        "physical_stock",
        "mismatch_qty",
        "supplier",
    ]
]

if mismatch_table.empty:
    st.success("All SKUs are matching with physical count.")
else:
    st.error("Mismatch found. These items need physical verification.")
    st.dataframe(mismatch_table, use_container_width=True, hide_index=True)

st.divider()

st.subheader("SKU-wise Stock Reconciliation")

display_columns = [
    "sku",
    "product_name",
    "category",
    "opening_stock",
    "inward_stock",
    "good_returns",
    "outward_stock",
    "damaged_stock",
    "calculated_closing_stock",
    "physical_stock",
    "mismatch_qty",
    "mismatch_status",
    "low_stock_status",
    "reorder_recommendation",
]

st.dataframe(
    filtered[display_columns],
    use_container_width=True,
    hide_index=True,
)

st.divider()

tab1, tab2, tab3 = st.tabs(
    ["Sales / Dispatch", "Returns & Damage", "Implementation Notes"]
)

with tab1:
    st.subheader("Sales and Dispatch Channel Summary")

    sales_data = stock_movements[stock_movements["movement_type"] == "SALE"]

    sales_summary = (
        sales_data.groupby("channel", as_index=False)["quantity"]
        .sum()
        .sort_values("quantity", ascending=False)
    )

    st.dataframe(sales_summary, use_container_width=True, hide_index=True)

    if not sales_summary.empty:
        fig_sales = px.bar(
            sales_summary,
            x="channel",
            y="quantity",
            text="quantity",
        )
        fig_sales.update_layout(
            xaxis_title="Channel",
            yaxis_title="Units Sold / Dispatched",
            height=330,
        )
        st.plotly_chart(fig_sales, use_container_width=True)

with tab2:
    st.subheader("Returns and Damaged Stock")

    returns_damage = stock_movements[
        stock_movements["movement_type"].isin(["RETURN", "DAMAGE"])
    ]

    st.dataframe(
        returns_damage[
            [
                "date",
                "sku",
                "movement_type",
                "channel",
                "quantity",
                "condition",
                "reference_id",
                "remarks",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

with tab3:
    st.subheader("How this system works")

    st.markdown(
        """
        This dashboard uses three simple data sources:

        - SKU Master: product details, opening stock, reorder level, supplier, cost.
        - Stock Movements: inward stock, sales, returns, damage, and adjustments.
        - Physical Count: actual warehouse/store count for mismatch checking.

        Closing stock formula:

        `Closing Stock = Opening + Inward + Good Returns - Sales - Damaged Stock`

        Practical deployment flow:

        - Warehouse team updates stock movements daily.
        - Shopify sales export can be imported into stock movements.
        - Bangalore store POS sales are added as daily sales.
        - Returned products are QC checked before adding back to sellable stock.
        - Dashboard flags low stock and mismatch items automatically.
        """
    )