# app.py
import streamlit as st
from database import init_db
from features import gold_in, gold_out, dashboard

# Initialize database
init_db()

# Sidebar navigation
st.sidebar.title("Gold Wallet")
page = st.sidebar.radio("Navigate to:", ["Dashboard", "Gold In", "Gold Out"])

if page == "Dashboard":
    dashboard.show_dashboard()
elif page == "Gold In":
    gold_in.handle_gold_in()
elif page == "Gold Out":
    gold_out.handle_gold_out()