# features/gold_out.py
import streamlit as st
from database import add_transaction

def handle_gold_out():
    sub_action = st.radio("Select Subaction:", ["Sell", "Pawn"])
    if sub_action == "Sell":
        st.header("Gold Out - Sell")
        asset_id = st.number_input("Asset ID", min_value=1, step=1)
        selling_price = st.number_input("Selling Price (RM)", min_value=0.0)
        date = st.date_input("Date")
        buyer_name = st.text_input("Buyer Name (optional)")
        notes = st.text_area("Notes (optional)")
        if st.button("Submit"):
            add_transaction(asset_id, "Sell", date, selling_price, f"Sold to {buyer_name}")
            st.success(f"Sell transaction recorded!")
    elif sub_action == "Pawn":
        st.header("Gold Out - Pawn")
        asset_id = st.number_input("Asset ID", min_value=1, step=1)
        loan_amount = st.number_input("Loan Amount (RM)", min_value=0.0)
        interest_rate = st.number_input("Interest Rate (%)", min_value=0.0)
        pawn_shop_name = st.text_input("Pawn Shop Name")
        maturity_date = st.date_input("Maturity Date")
        date = st.date_input("Date")
        if st.button("Submit"):
            add_transaction(asset_id, "Pawn", date, loan_amount, f"Pawned at {pawn_shop_name}")
            st.success(f"Pawn transaction recorded at {pawn_shop_name}")