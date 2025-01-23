import streamlit as st
from database import fetch_asset_summary, render_asset_summary_with_tags, fetch_transactions

def show_dashboard():
    # Render asset summary with tagging feature
    st.header("Asset Summary")
    assets = fetch_asset_summary()
    if assets:
        render_asset_summary_with_tags(assets)
    else:
        st.write("No assets found.")

    # Render transaction history
    st.header("Transaction History")
    transactions = fetch_transactions()
    if transactions:
        for t in transactions:
            st.write(f"Transaction ID: {t[0]} | Type: {t[1]} | Date: {t[2]} | Amount: RM {t[3]:.2f} | Notes: {t[4]}")
    else:
        st.write("No transactions recorded.")
