import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Churn Analytics Dashboard", layout="wide")

st.title("📊 Customer Churn Interactive Analytics Dashboard")

# ==============================
# Load Data
# ==============================
@st.cache_data
def load_data():
    return pd.read_csv("data/raw/Telco-Customer-Churn.csv")

df = load_data()
df["ChurnBinary"] = df["Churn"].map({"Yes": 1, "No": 0})

# ==============================
# Sidebar Filters
# ==============================
st.sidebar.header("🔎 Filter Customers")

contract_filter = st.sidebar.multiselect(
    "Select Contract Type",
    options=df["Contract"].unique(),
    default=df["Contract"].unique()
)

internet_filter = st.sidebar.multiselect(
    "Select Internet Service",
    options=df["InternetService"].unique(),
    default=df["InternetService"].unique()
)

tenure_range = st.sidebar.slider(
    "Select Tenure Range (months)",
    min_value=int(df["tenure"].min()),
    max_value=int(df["tenure"].max()),
    value=(0, 72)
)

# Apply filters
filtered_df = df[
    (df["Contract"].isin(contract_filter)) &
    (df["InternetService"].isin(internet_filter)) &
    (df["tenure"] >= tenure_range[0]) &
    (df["tenure"] <= tenure_range[1])
]

# ==============================
# Dynamic KPIs
# ==============================
st.subheader("📌 Segment KPIs")

total_customers = len(filtered_df)
churn_rate = filtered_df["ChurnBinary"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Customers in Segment", total_customers)
col2.metric("Segment Churn Rate", f"{churn_rate:.2%}" if total_customers > 0 else "N/A")
col3.metric("Churned Customers", int(filtered_df["ChurnBinary"].sum()))

st.divider()

# ==============================
# Normalized Contract Churn
# ==============================
st.subheader("📄 Churn Rate by Contract (Segment View)")

if total_customers > 0:
    contract_churn = pd.crosstab(
        filtered_df["Contract"],
        filtered_df["Churn"],
        normalize="index"
    )

    st.dataframe(contract_churn)

    fig1, ax1 = plt.subplots()
    contract_churn["Yes"].plot(kind="bar", ax=ax1)
    ax1.set_ylabel("Churn Rate")
    st.pyplot(fig1)
else:
    st.warning("No customers match selected filters.")

st.divider()

# ==============================
# Tenure Distribution
# ==============================
st.subheader("⏳ Tenure Distribution (Filtered)")

if total_customers > 0:
    fig2, ax2 = plt.subplots()
    sns.boxplot(data=filtered_df, x="Churn", y="tenure", ax=ax2)
    st.pyplot(fig2)

st.divider()

# ==============================
# Internet Service Analysis
# ==============================
st.subheader("🌐 Internet Service vs Churn (Filtered)")

if total_customers > 0:
    fig3, ax3 = plt.subplots()
    sns.countplot(data=filtered_df, x="InternetService", hue="Churn", ax=ax3)
    st.pyplot(fig3)

st.divider()

# ==============================
# Executive Insight
# ==============================
st.subheader("📊 Business Insight")

st.markdown("""
This interactive dashboard allows exploration of churn risk across:

- Contract types
- Internet service categories
- Customer tenure segments

By filtering customer groups, decision-makers can identify high-risk segments and 
prioritize retention campaigns accordingly.
""")
