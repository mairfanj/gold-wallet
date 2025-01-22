def calculate_wealth(data):
    """Calculate the total wealth from all records."""
    if data is None or data.empty:
        return 0
    return data["Price (RM)"].sum()

def calculate_zakat(total_wealth):
    """Calculate zakat based on total wealth."""
    nisab_threshold = 85 * 300  # Approximate gold nisab in RM
    zakat_rate = 0.025
    return total_wealth * zakat_rate if total_wealth > nisab_threshold else 0
