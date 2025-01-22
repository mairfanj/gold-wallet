import streamlit as st
import pandas as pd
from utils.file_handler import load_data, add_record
from utils.calculations import calculate_wealth, calculate_zakat

# App Title
st.title("Gold Wallet")
st.write("Manage your gold transactions, track wealth, and calculate zakat.")

# Sidebar Menu
menu = st.sidebar.selectbox("Menu", ["Home", "Add Record", "View Records", "Wealth & Zakat"])

# Load Data
data_file = "data/jewelry_records.csv"
data = load_data(data_file)

if menu == "Home":
    st.header("Welcome to Gold Wallet")
    st.write("Start tracking your gold transactions and financial data.")

elif menu == "Add Record":
    st.header("Add a New Jewelry Record")
    with st.form("add_record_form"):
        date = st.date_input("Date")
        transaction_type = st.selectbox("Transaction Type", ["Buy", "Sell", "Pajak", "Gadai", "Tebus"])
        price = st.number_input("Price (RM)", min_value=0.0, step=0.1)
        weight = st.number_input("Weight (grams)", min_value=0.0, step=0.1)
        jewelry_type = st.text_input("Jewelry Type (e.g., Ring, Bracelet)")
        shop_name = st.text_input("Shop Name")
        submitted = st.form_submit_button("Add Record")

        if submitted:
            record = {
                "Date": str(date),
                "Transaction Type": transaction_type,
                "Price (RM)": price,
                "Weight (grams)": weight,
                "Type": jewelry_type,
                "Shop Name": shop_name
            }
            add_record(data_file, record)
            st.success("Record added successfully!")

elif menu == "View Records":
    st.header("View All Records")
    if data is not None:
        st.dataframe(data)
    else:
        st.write("No records found. Add some records to get started.")

elif menu == "Wealth & Zakat":
    st.header("Wealth & Zakat Calculation")
    total_wealth = calculate_wealth(data)
    zakat = calculate_zakat(total_wealth)
    st.write(f"**Total Wealth:** RM {total_wealth:.2f}")
    st.write(f"**Zakat Payable:** RM {zakat:.2f}")
