import sqlite3

# Ensure the assets table has the `tag` column
def alter_assets_table():
    conn = sqlite3.connect("gold_wallet.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
        ALTER TABLE assets ADD COLUMN tag TEXT
        """)
        conn.commit()
        print("Tag column added to assets table.")
    except sqlite3.OperationalError:
        print("Tag column already exists or another issue occurred.")
    finally:
        conn.close()

alter_assets_table()

# Initialize the database
def init_db():
    conn = sqlite3.connect("gold_wallet.db")
    cursor = conn.cursor()

    # Create assets table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assets (
        asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        weight REAL,
        initial_price REAL,
        current_status TEXT,
        tag TEXT
    )
    """)

    # Create transactions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_id INTEGER,
        transaction_type TEXT,
        transaction_date DATE,
        amount REAL,
        notes TEXT,
        FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
    )
    """)

    conn.commit()
    conn.close()

# Add a new asset to the database
def add_asset(name, weight, initial_price, status, tag):
    conn = sqlite3.connect("gold_wallet.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO assets (name, weight, initial_price, current_status, tag)
    VALUES (?, ?, ?, ?, ?)
    """, (name, weight, initial_price, status, tag))
    conn.commit()
    asset_id = cursor.lastrowid
    conn.close()
    return asset_id

# Add a transaction to the database
def add_transaction(asset_id, transaction_type, transaction_date, amount, notes):
    conn = sqlite3.connect("gold_wallet.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO transactions (asset_id, transaction_type, transaction_date, amount, notes)
    VALUES (?, ?, ?, ?, ?)
    """, (asset_id, transaction_type, transaction_date, amount, notes))

    # Update asset status
    new_status = ""
    if transaction_type == "Buy":
        new_status = "Owned"
    elif transaction_type == "Redeem":
        new_status = "Owned"
    elif transaction_type == "Sell":
        new_status = "Sold"
    elif transaction_type == "Pawn":
        new_status = "Pawned"

    if new_status:
        cursor.execute("""
        UPDATE assets
        SET current_status = ?
        WHERE asset_id = ?
        """, (new_status, asset_id))

    conn.commit()
    conn.close()

# Fetch all assets from the database
def fetch_asset_summary():
    conn = sqlite3.connect("gold_wallet.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT asset_id, name, weight, current_status, tag
    FROM assets
    """)
    data = cursor.fetchall()
    conn.close()
    return data

# Fetch transactions from the database
def fetch_transactions(transaction_type=None):
    conn = sqlite3.connect("gold_wallet.db")
    cursor = conn.cursor()
    query = """
    SELECT t.transaction_id, t.transaction_type, t.transaction_date, t.amount, t.notes, a.name
    FROM transactions t
    JOIN assets a ON t.asset_id = a.asset_id
    """
    if transaction_type:
        query += " WHERE t.transaction_type = ?"
        cursor.execute(query, (transaction_type,))
    else:
        cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

# Render asset summary with tags in a neat, bordered table
def render_asset_summary_with_tags(assets):
    import streamlit as st
    import pandas as pd
    import random

    # Prepare asset data
    asset_data = []
    for asset in assets:
        asset_id = asset[0]
        tags = asset[4] or "Add Tag"
        asset_data.append({
            "Asset ID": asset[0],
            "Name": asset[1],
            "Weight (g)": asset[2],
            "Status": asset[3],
            "Tags": tags
        })

    # Convert to DataFrame for rendering
    df = pd.DataFrame(asset_data)

    st.write("### Asset Summary")

    # Render the DataFrame as a styled table
    for _, row in df.iterrows():
        col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 3])
        col1.write(f"**{row['Asset ID']}**")
        col2.write(row['Name'])
        col3.write(f"{row['Weight (g)']}g")
        col4.write(row['Status'])

        # Render Tags with inline editing
        with col5:
            tags = row['Tags'].split(",") if row['Tags'] != "Add Tag" else []
            tag_input = st.text_input(
                label="",
                value=", ".join(tags),
                placeholder="Add Tag",
                key=f"tag_input_{row['Asset ID']}"
            )

            # Display tags as colored labels
            for tag in tags:
                color = f"#{random.randint(0, 0xFFFFFF):06x}"  # Random color
                st.markdown(
                    f'<span style="background-color:{color}; color:white; border-radius:3px; padding:2px 5px; margin-right:5px; display:inline-block;">{tag}</span>',
                    unsafe_allow_html=True
                )

            # Update tags on input change
            if tag_input != row['Tags']:
                conn = sqlite3.connect("gold_wallet.db")
                cursor = conn.cursor()
                cursor.execute("""
                UPDATE assets
                SET tag = ?
                WHERE asset_id = ?
                """, (tag_input, row['Asset ID']))
                conn.commit()
                conn.close()
                st.success(f"Tags updated for Asset ID {row['Asset ID']}!")

