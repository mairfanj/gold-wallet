import pandas as pd

def calculate_wealth(data):
    """Calculate the total wealth from all records."""
    if data is None or data.empty:
        return 0
    return data["Price (RM)"].sum()

def calculate_zakat(data, zakat_rates_file):
    """Calculate Zakat based on yearly gold price and rates."""
    try:
        zakat_rates = pd.read_csv(zakat_rates_file)
    except FileNotFoundError:
        zakat_rates = pd.DataFrame(columns=["Year", "Gold Price (RM/gram)", "Zakat Rate (%)"])

    total_zakat = 0
    if data is not None and not data.empty:
        for _, row in data.iterrows():
            transaction_year = pd.to_datetime(row["Date"]).year
            weight = row["Weight (grams)"]
            gold_price = zakat_rates.loc[zakat_rates["Year"] == transaction_year, "Gold Price (RM/gram)"].values
            zakat_rate = zakat_rates.loc[zakat_rates["Year"] == transaction_year, "Zakat Rate (%)"].values

            if gold_price.size > 0 and zakat_rate.size > 0:
                gold_price = gold_price[0]
                zakat_rate = zakat_rate[0] / 100
                total_value = weight * gold_price
                nisab_value = 85 * gold_price
                if total_value > nisab_value:
                    total_zakat += total_value * zakat_rate

    return total_zakat

def calculate_yearly_zakat(data, zakat_rates_file):
    """Calculate Zakat payable for each year."""
    try:
        zakat_rates = pd.read_csv(zakat_rates_file)
    except FileNotFoundError:
        zakat_rates = pd.DataFrame(columns=["Year", "Gold Price (RM/gram)", "Zakat Rate (%)"])

    yearly_zakat = []
    if data is not None and not data.empty:
        for year in data["Date"].apply(lambda x: pd.to_datetime(x).year).unique():
            year_data = data[pd.to_datetime(data["Date"]).dt.year == year]
            weight = year_data["Weight (grams)"].sum()
            gold_price = zakat_rates.loc[zakat_rates["Year"] == year, "Gold Price (RM/gram)"].values
            zakat_rate = zakat_rates.loc[zakat_rates["Year"] == year, "Zakat Rate (%)"].values

            if gold_price.size > 0 and zakat_rate.size > 0:
                gold_price = gold_price[0]
                zakat_rate = zakat_rate[0] / 100
                total_value = weight * gold_price
                nisab_value = 85 * gold_price

                zakat_amount = total_value * zakat_rate if total_value > nisab_value else 0
                yearly_zakat.append({"Year": year, "Zakat Amount": zakat_amount})

    return pd.DataFrame(yearly_zakat)
