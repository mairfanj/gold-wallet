import streamlit as st
import pandas as pd
from utils.file_handler import load_data, save_data, add_record
from utils.calculations import calculate_wealth, calculate_zakat

# File path for CSV
data_file = "data/jewelry_records.csv"

# Load data
data = load_data(data_file)

# Sidebar Menu
menu = st.sidebar.selectbox("Menu", ["Home", "Add Record", "View Records", "Wealth & Zakat", "Edit Item"])

if menu == "Home":
    st.title("Gold Wallet")
    st.write("Track your gold transactions, calculate wealth, and determine zakat.")

elif menu == "Add Record":
    st.header("Add a New Jewelry Record")
    with st.form("add_record_form"):
        date = st.date_input("Date")
        transaction_type = "Buy"  # Only "Buy" is allowed for adding records
        price = st.number_input("Price (RM)", min_value=0.0, step=0.1)
        weight = st.number_input("Weight (grams)", min_value=0.0, step=0.1)
        jewelry_type = st.text_input("Jewelry Type (e.g., Ring, Bracelet)")
        shop_name = st.text_input("Shop Name")
        submitted = st.form_submit_button("Add Record")

        if submitted:
            new_record = {
                "Date": str(date),
                "Transaction Type": transaction_type,
                "Price (RM)": price,
                "Weight (grams)": weight,
                "Type": jewelry_type,
                "Shop Name": shop_name,
                "Notes": ""
            }
            add_record(data_file, new_record)
            st.success("Record added successfully!")

elif menu == "View Records":
    st.header("View All Records")
    if data is not None and not data.empty:
        st.dataframe(data)
    else:
        st.write("No records found. Add some records to get started.")

elif menu == "Wealth & Zakat":
    st.header("Wealth & Zakat Calculation")
    if data is not None and not data.empty:
        total_wealth = calculate_wealth(data)
        zakat = calculate_zakat(total_wealth)
        st.write(f"**Total Wealth:** RM {total_wealth:.2f}")
        st.write(f"**Zakat Payable:** RM {zakat:.2f}")
    else:
        st.write("No data available to calculate wealth or zakat.")

elif menu == "Edit Item":
    st.header("Edit Item")
    if data is not None and not data.empty:
        # Select an item to edit
        st.write("Select an item to edit:")
        record_index = st.selectbox(
            "Choose a record", 
            data.index, 
            format_func=lambda i: f"{data.loc[i, 'Type']} - {data.loc[i, 'Date']}"
        )

        # Display the selected record
        selected_record = data.loc[record_index]
        st.write("Current Details:")
        st.write(selected_record)

        # Form for editing the item
        with st.form("edit_item_form"):
            transaction_type = st.selectbox(
                "Transaction Type", 
                ["Buy", "Sell", "Pajak", "Gadai", "Tebus"], 
                index=["Buy", "Sell", "Pajak", "Gadai", "Tebus"].index(selected_record["Transaction Type"])
            )
            update_date = st.date_input("Transaction Date", value=pd.to_datetime(selected_record["Date"]))
            update_price = st.number_input(
                "Transaction Price (RM)", 
                value=selected_record["Price (RM)"], 
                min_value=0.0, 
                step=0.1
            )
            notes = st.text_area("Notes", value=selected_record.get("Notes", ""))

            # Submit button
            submitted = st.form_submit_button("Save Changes")
            if submitted:
                # Update the record in the DataFrame
                data.at[record_index, "Transaction Type"] = transaction_type
                data.at[record_index, "Date"] = str(update_date)
                data.at[record_index, "Price (RM)"] = update_price
                data.at[record_index, "Notes"] = notes

                # Save updated data
                save_data(data_file, data)
                st.success("Item updated successfully!")
    else:
        st.write("No records found. Please add some records first.")
