# features/gold_in.py
import streamlit as st
from database import add_transaction, add_asset

def handle_gold_in():
    sub_action = st.radio("Select Subaction:", ["Buy", "Redeem"])
    if sub_action == "Buy":
        st.header("Gold In - Buy")
        name = st.text_input("Name/Type of Asset")
        weight = st.number_input("Weight (grams)", min_value=0.0)
        price = st.number_input("Price (RM)", min_value=0.0)
        date = st.date_input("Date")
        shop_name = st.text_input("Shop Name")
        if st.button("Submit"):
            asset_id = add_asset(name, weight, price, "Owned")
            add_transaction(asset_id, "Buy", date, price, f"Bought from {shop_name}")
            st.success(f"Buy transaction recorded: {name}")
    elif sub_action == "Redeem":
        st.header("Gold In - Redeem")
        asset_id = st.number_input("Asset ID", min_value=1, step=1)
        loan_amount = st.number_input("Loan Amount (RM)", min_value=0.0)
        additional_costs = st.number_input("Additional Costs (RM)", min_value=0.0)
        date = st.date_input("Date")
        pawn_shop_name = st.text_input("Pawn Shop Name")
        notes = st.text_area("Notes (optional)")
        if st.button("Submit"):
            add_transaction(asset_id, "Redeem", date, loan_amount + additional_costs, f"Redeemed from {pawn_shop_name}")
            st.success(f"Redeem transaction recorded at {pawn_shop_name}")