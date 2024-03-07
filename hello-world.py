import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe

def create_bystate_df(df):
    bystate_df = df.groupby(by="customer_state").customer_id.nunique().reset_index()
    bystate_df.rename(columns={
    "customer_id": "customer_count"
}, inplace=True)
    
    return bystate_df

def create_bypayment_df(df):
    bypayment_df = all_df.groupby(by="payment_type").customer_id.nunique().reset_index()
    bypayment_df.rename(columns={
    "customer_id": "customer_count"
}, inplace=True)
    
    return bypayment_df


# Load cleaned data
all_df = pd.read_csv("C:\\Users\\user\\OneDrive\\Documents\\Bagus\\Kuliah\\Ecommerce\\all_data_fp.csv")

datetime_columns = ["order_purchase_timestamp", "order_approved_at","order_delivered_carrier_date","order_delivered_customer_date","order_estimated_delivery_date"]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Filter data
min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://w7.pngwing.com/pngs/713/936/png-transparent-online-shopping-shopping-cart-logo-e-commerce-market-blue-angle-company.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                (all_df["order_purchase_timestamp"] <= str(end_date))]

# st.dataframe(main_df)

# # Menyiapkan berbagai dataframe
bypayment_df = create_bypayment_df(main_df)
bystate_df = create_bystate_df(main_df)


# plot number of daily orders (2021)
st.header('Public E-Commerce')

# customer payment type
st.subheader("Customer Payment Type")

fig, ax = plt.subplots(figsize=(20, 10))

sns.barplot(
        y="customer_count", 
        x="payment_type",
        data=bypayment_df.sort_values(by="customer_count", ascending=False),
        ax=ax

    )
ax.set_title("Number of Customer by Payment Type", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)


# customer payment type

st.subheader("Customer State")

fig, ax = plt.subplots(figsize=(20, 10))

colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
        x="customer_count", 
        y="customer_state",
        data=bystate_df.sort_values(by="customer_count", ascending=False),

    )
ax.set_title("Number of Customer by State", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

st.caption('Bagus Adi Cahyono Heksa')