import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Load Excel file
@st.cache_data
def load_data():
    df = pd.read_excel("fiep_npv_calculator.xlsx", sheet_name="Tabelle1")
    cashflows = df.iloc[2:, [0, 1, 2]].copy()
    cashflows.columns = ["Year", "Startup", "Cash Cow"]
    cashflows = cashflows.dropna()
    cashflows = cashflows.astype({"Year": int, "Startup": float, "Cash Cow": float})
    return cashflows

cashflows = load_data()

# Sidebar: Discount rate slider
r = st.sidebar.slider("Zinssatz (Discount Rate)", min_value=0.0, max_value=0.3, value=0.1, step=0.01)

# Calculate discounted cash flows
years_from_start = np.arange(len(cashflows))
discount_factors = 1 / (1 + r) ** years_from_start
startup_discounted = cashflows["Startup"] * discount_factors
cashcow_discounted = cashflows["Cash Cow"] * discount_factors

# Show NPVs
npv_startup = startup_discounted.sum()
npv_cashcow = cashcow_discounted.sum()
st.write(f"**NPV Startup:** {npv_startup:.2f} €")
st.write(f"**NPV Cash Cow:** {npv_cashcow:.2f} €")

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(cashflows["Year"]))
width = 0.4
ax.bar(x - width/2, startup_discounted, width=width, label="Startup (diskontiert)")
ax.bar(x + width/2, cashcow_discounted, width=width, label="Cash Cow (diskontiert)")
ax.set_xticks(x)
ax.set_xticklabels(cashflows["Year"])
ax.set_title(f"Diskontierte Cashflows bei Zinssatz = {r*100:.1f}%")
ax.set_xlabel("Jahr")
ax.set_ylabel("Diskontierter Cashflow")
ax.legend()
ax.grid(True)

st.pyplot(fig)
