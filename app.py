import streamlit as st
import pandas as pd
import os
from utils.file_handler import load_data, save_data
from utils.calculations import calculate_wealth, calculate_zakat, calculate_yearly_zakat

# File paths
data_file = "data/jewelry_records.csv"
zakat_rates_file = "data/zakat_rates.csv"

# Load data
data = load_data(data_file)

# Sidebar Menu
menu = st.sidebar.selectbox("Menu", ["Home", "Add Record", "View Records", "Wealth & Zakat", "Manage Zakat Rates", "Edit Item"])

if menu == "Home":
    st.title("Gold Wallet")
    st.write("Track your gold transactions, calculate wealth, and determine zakat.")

elif menu == "Add Record":
    st.header("Add a New Jewelry Record")
    with st.form("add_record_form"):
        date = st.date_input("Date")
        transaction_type = st.selectbox("Transaction Type", ["Buy", "Pawn", "Sell", "Redeem"])
        price = st.number_input("Price (RM)", min_value=0.0, step=0.1)
        weight = st.number_input("Weight (grams)", min_value=0.0, step=0.1)
        jewelry_type = st.text_input("Jewelry Type (e.g., Ring, Bracelet)")
        shop_name = st.text_input("Shop Name")
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Add Record")

        if submitted:
            new_record = {
                "Date": str(date),
                "Transaction Type": transaction_type,
                "Price (RM)": price,
                "Weight (grams)": weight,
                "Type": jewelry_type,
                "Shop Name": shop_name,
                "Notes": notes
            }
            save_data(data_file, pd.DataFrame([new_record]))
            st.success("Record added successfully!")

elif menu == "View Records":
    st.header("View All Records")
    if data is not None and not data.empty:
        data_display = data.copy()
        data_display.index = data_display.index + 1
        st.dataframe(data_display)
    else:
        st.write("No records found. Please add some records first.")

elif menu == "Wealth & Zakat":
    st.header("Wealth & Zakat Calculation")

    if data is not None and not data.empty:
        data["Date"] = pd.to_datetime(data["Date"])
        data["Year"] = data["Date"].dt.year

        # Calculate cumulative weight and zakat payable for each year
        yearly_weight = data.groupby("Year")[["Weight (grams)"]].sum().cumsum().reset_index()
        yearly_weight.rename(columns={"Weight (grams)": "Cumulative Weight (grams)"}, inplace=True)

        # Load zakat rates
        zakat_rates = pd.read_csv(zakat_rates_file)
        zakat_summary = yearly_weight.merge(zakat_rates, on="Year", how="left")
        zakat_summary["Zakat Payable"] = zakat_summary.apply(
            lambda row: row["Cumulative Weight (grams)"] * row["Gold Price (RM/gram)"] * row["Zakat Rate (%)"] / 100
            if row["Cumulative Weight (grams)"] >= 85 else 0,
            axis=1
        )

        # Manage payment status
        zakat_status_file = "data/zakat_status.csv"
        if not os.path.exists(zakat_status_file):
            zakat_summary["Paid"] = "Not Paid Yet"
            zakat_summary.to_csv(zakat_status_file, index=False)
        else:
            zakat_status = pd.read_csv(zakat_status_file)
            zakat_summary = zakat_summary.merge(zakat_status[["Year", "Paid"]], on="Year", how="left")

        # Display all data in a table view
        st.subheader("Yearly Zakat Summary")
        st.write("Below is a comprehensive summary of cumulative weight, zakat payable, and payment status for each year:")
        st.dataframe(zakat_summary[["Year", "Cumulative Weight (grams)", "Gold Price (RM/gram)", "Zakat Rate (%)", "Zakat Payable", "Paid"]])

        # Update payment status
        st.write("### Update Zakat Payment Status")
        for _, row in zakat_summary.iterrows():
            new_status = st.radio(
                f"Update Status for {row['Year']}",
                options=["Paid", "Not Paid Yet"],
                index=0 if row["Paid"] == "Paid" else 1,
                key=row["Year"]
            )

            if new_status != row["Paid"]:
                zakat_summary.loc[zakat_summary["Year"] == row["Year"], "Paid"] = new_status
                zakat_summary.to_csv(zakat_status_file, index=False)
                st.success(f"Updated Zakat status for {row['Year']} to {new_status}.")

        # Display wealth summary
        total_wealth = calculate_wealth(data)
        total_paid_zakat = zakat_summary.loc[zakat_summary["Paid"] == "Paid", "Zakat Payable"].sum()
        updated_wealth = total_wealth - total_paid_zakat

        st.write("### Wealth Summary")
        st.write(f"**Total Wealth Before Zakat:** RM {total_wealth:.2f}")
        st.write(f"**Total Zakat Paid:** RM {total_paid_zakat:.2f}")
        st.write(f"**Updated Wealth After Zakat:** RM {updated_wealth:.2f}")

    else:
        st.write("No data available to calculate wealth or zakat.")

elif menu == "Manage Zakat Rates":
    st.header("Manage Zakat Rates")
    try:
        zakat_rates = pd.read_csv(zakat_rates_file)
    except FileNotFoundError:
        zakat_rates = pd.DataFrame(columns=["Year", "Gold Price (RM/gram)", "Zakat Rate (%)"])

    st.write("Current Zakat Rates:")
    if not zakat_rates.empty:
        st.dataframe(zakat_rates)
    else:
        st.write("No Zakat rates found. Please add rates for each year.")

    with st.form("add_zakat_rate_form"):
        year = st.number_input("Year", min_value=2000, max_value=2100, step=1)
        gold_price = st.number_input("Gold Price (RM/gram)", min_value=0.0, step=0.1)
        zakat_rate = st.number_input("Zakat Rate (%)", min_value=0.0, step=0.1)
        submitted = st.form_submit_button("Save Zakat Rate")

        if submitted:
            if year in zakat_rates["Year"].values:
                zakat_rates.loc[zakat_rates["Year"] == year, ["Gold Price (RM/gram)", "Zakat Rate (%)"]] = [gold_price, zakat_rate]
                st.success(f"Updated Zakat rate for {year}.")
            else:
                zakat_rates = zakat_rates.append({"Year": year, "Gold Price (RM/gram)": gold_price, "Zakat Rate (%)": zakat_rate}, ignore_index=True)
                st.success(f"Added Zakat rate for {year}.")

            zakat_rates.to_csv(zakat_rates_file, index=False)

elif menu == "Edit Item":
    st.header("Edit Item")
    if data is not None and not data.empty:
        record_index = st.selectbox("Choose a record", data.index, format_func=lambda i: f"{data.loc[i, 'Type']} - {data.loc[i, 'Weight (grams)']}g")
        selected_record = data.loc[record_index]
        st.write("Current Details:")
        st.write(selected_record)

        with st.form("edit_item_form"):
            transaction_type = st.selectbox("Transaction Type", ["Buy", "Pawn", "Sell", "Redeem"], index=["Buy", "Pawn", "Sell", "Redeem"].index(selected_record["Transaction Type"]))
            update_date = st.date_input("Transaction Date", value=pd.to_datetime(selected_record["Date"]))
            update_price = st.number_input("Transaction Price (RM)", value=selected_record["Price (RM)"], min_value=0.0, step=0.1)
            weight = st.number_input("Weight (grams)", value=selected_record["Weight (grams)"], min_value=0.0, step=0.1)
            jewelry_type = st.text_input("Jewelry Type (e.g., Ring, Bracelet)", value=selected_record["Type"])
            shop_name = st.text_input("Shop Name", value=selected_record["Shop Name"])
            notes = st.text_area("Notes", value=selected_record.get("Notes", ""))
            submitted = st.form_submit_button("Save Changes")
            remove_item = st.form_submit_button("Remove This Item", type="secondary")

            if submitted:
                data.at[record_index, "Transaction Type"] = transaction_type
                data.at[record_index, "Date"] = str(update_date)
                data.at[record_index, "Price (RM)"] = update_price
                data.at[record_index, "Weight (grams)"] = weight
                data.at[record_index, "Type"] = jewelry_type
                data.at[record_index, "Shop Name"] = shop_name
                data.at[record_index, "Notes"] = notes
                save_data(data_file, data)
                st.success("Item updated successfully!")

            if remove_item:
                data.drop(record_index, inplace=True)
                save_data(data_file, data)
                st.warning("Item removed successfully!")
    else:
        st.write("No records available. Please add some records first.")
