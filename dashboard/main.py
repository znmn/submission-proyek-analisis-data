import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# load necessary data
orders = pd.read_csv('orders.csv')
orders_customers = pd.read_csv('orders_customers.csv')
total_order_by_payment_type = pd.read_csv('total_order_by_payment_type.csv')
total_revenue_per_category = pd.read_csv('total_revenue_per_category.csv')

# convert to datetime
datetime_cols = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date",
                 "order_delivered_customer_date", "order_estimated_delivery_date"]
for col in datetime_cols:
    orders[col] = pd.to_datetime(orders[col])
orders_customers["order_purchase_timestamp"] = pd.to_datetime(
    orders_customers["order_purchase_timestamp"])


def show_total_order_by_payment_type(df):
    fig, ax = plt.subplots(figsize=(10, 6))

    colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(data=df, x="total_order", y="payment_type",
                hue="payment_type", palette=colors_, ax=ax)
    ax.set_title("Total Order by Payment Type")
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    return fig


def show_late_delivery_precentage(df):
    late_delivery_order_percentage = df["is_late"].mean() * 100
    fig, ax = plt.subplots(figsize=(8, 8))

    labels = ["On Time", "Late"]
    colors = ["lightgreen", "lightcoral"]
    ax.pie([1 - late_delivery_order_percentage / 100, late_delivery_order_percentage / 100], labels=labels, colors=colors,
           autopct='%1.1f%%', startangle=140)
    ax.set_title("Late Delivery Order Percentage")
    return fig


def show_total_revenue_per_category(df, mode="top"):
    colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    fig, ax = plt.subplots(figsize=(16, 8))

    if mode == "top":
        sns.barplot(x="total_revenue",
                    y="product_category_name", hue="product_category_name", data=df.head(5), palette=colors_, ax=ax)
        plt.suptitle("Top 5 Total Revenue per Category", fontsize=18)
    else:
        sns.barplot(x="total_revenue",
                    y="product_category_name", hue="product_category_name", data=df.sort_values(
                        by="total_revenue", ascending=True).head(5), palette=colors_, ax=ax)
        ax.invert_xaxis()
        ax.yaxis.set_label_position("right")
        ax.yaxis.tick_right()
        plt.suptitle("Bottom 5 Total Revenue per Category", fontsize=18)

    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.tick_params(axis="y", labelsize=15)

    return fig


def show_rfm_analysis(df, metric="Recency"):
    fig, ax = plt.subplots(figsize=(10, 6))
    colors_ = ["#72BCD4"] * 5

    if metric == "Recency":
        sns.barplot(y="recency", x="customer_unique_id", hue="customer_unique_id",
                    data=df.sort_values(by="recency", ascending=True).head(5), palette=colors_, ax=ax)
        ax.set_ylabel(None)
        ax.set_xlabel(None)
        ax.set_title("By Recency (days)", loc="center", fontsize=18)
        ax.tick_params(axis="x", labelsize=10)
    elif metric == "Frequency":
        sns.barplot(y="frequency", x="customer_unique_id", hue="customer_unique_id",
                    data=df.sort_values(by="frequency", ascending=False).head(5), palette=colors_, ax=ax)
        ax.set_ylabel(None)
        ax.set_xlabel(None)
        ax.set_title("By Frequency", loc="center", fontsize=18)
        ax.tick_params(axis="x", labelsize=10)
    elif metric == "Monetary":
        sns.barplot(y="monetary", x="customer_unique_id", hue="customer_unique_id",
                    data=df.sort_values(by="monetary", ascending=False).head(5), palette=colors_, ax=ax)
        ax.set_ylabel(None)
        ax.set_xlabel(None)
        ax.set_title("By Monetary", loc="center", fontsize=18)
        ax.tick_params(axis="x", labelsize=10)

    fig.suptitle("Top 5 Customers Based on RFM Parameters", fontsize=20)
    return fig


# sidebar
with st.sidebar:
    st.image(
        "https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.svg")
    st.write('Nama: **Zainul Muhaimin**')
    st.write(
        'ID Dicoding: **[zainul-muhaimin](https://www.dicoding.com/users/zainul-muhaimin)**')

# header
st.header('E-commerce Data Analytics Dashboard :sparkles:')

# section Total Order by Payment Type
st.subheader('Total Order by Payment Type')
col1, col2 = st.columns(2)
with col1:
    max_total_order = total_order_by_payment_type["total_order"].max()
    st.write(f"Max Total Order: **{max_total_order}**")
with col2:
    min_total_order = total_order_by_payment_type["total_order"].min()
    st.write(f"Min Total Order: **{min_total_order}**")
fig = show_total_order_by_payment_type(total_order_by_payment_type)
st.pyplot(fig)

# section Late Delivery Order Percentage
st.subheader('Late Delivery Order Percentage')
col1, col2 = st.columns(2)
with col1:
    total_order = orders.shape[0]
    st.write(f"Total Order: **{total_order}**")
with col2:
    late_delivery_order = orders["is_late"].sum()
    st.write(f"Late Delivery Order: **{late_delivery_order}**")
fig = show_late_delivery_precentage(orders)
st.pyplot(fig)

# section Total Revenue per Category
st.subheader('Total Revenue per Category')
col1, col2 = st.columns(2)
tab1, tab2 = st.tabs(["Top 5", "Bottom 5"])
fig1, fig2 = show_total_revenue_per_category(
    total_revenue_per_category, "top"), show_total_revenue_per_category(total_revenue_per_category, "bottom")
with col1:
    max_total_revenue = total_revenue_per_category["total_revenue"].max()
    st.write(f"Max Total Revenue: **{max_total_revenue}**")
with col2:
    min_total_revenue = total_revenue_per_category["total_revenue"].min()
    st.write(f"Min Total Revenue: **{min_total_revenue}**")
tab1.pyplot(fig1)
tab2.pyplot(fig2)

# section RFM Analysis
st.subheader('RFM Analysis')
tab1, tab2, tab3 = st.tabs(["Recency", "Frequency", "Monetary"])
fig1, fig2, fig3 = show_rfm_analysis(orders_customers, "Recency"), show_rfm_analysis(
    orders_customers, "Frequency"), show_rfm_analysis(orders_customers, "Monetary")
tab1.pyplot(fig1)
tab2.pyplot(fig2)
tab3.pyplot(fig3)
