import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# 🎯 Page setup
# ---------------------------------------------------------
st.set_page_config(
    page_title="Clinical Trials Dashboard",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 Clinical Trials Analytics Dashboard")
st.markdown("Explore global **clinical trial activity** by condition, country, and phase.")

# ---------------------------------------------------------
# 📦 Load data
# ---------------------------------------------------------
conn = sqlite3.connect("clinical_trials.db")
df = pd.read_sql_query("SELECT * FROM site_analysis", conn)
conn.close()

if df.empty:
    st.error("No data found in the database. Please run `main.py` first.")
    st.stop()

# ---------------------------------------------------------
# 🧹 Preprocess
# ---------------------------------------------------------
df["country"] = df["country"].fillna("Unknown")
df["trial_count"] = pd.to_numeric(df["trial_count"], errors="coerce").fillna(0).astype(int)

# ---------------------------------------------------------
# 🎛️ Filters
# ---------------------------------------------------------
st.sidebar.header("🔍 Filters")
selected_country = st.sidebar.multiselect(
    "Select Country", sorted(df["country"].unique()), default=None
)
min_studies = st.sidebar.slider("Minimum Study Count", 0, int(df["trial_count"].max()), 1)

filtered_df = df.copy()
if selected_country:
    filtered_df = filtered_df[filtered_df["country"].isin(selected_country)]
filtered_df = filtered_df[filtered_df["trial_count"] >= min_studies]

# ---------------------------------------------------------
# 🔢 KPI Cards
# ---------------------------------------------------------
total_sites = len(filtered_df)
total_trials = filtered_df["trial_count"].sum()
unique_countries = filtered_df["country"].nunique()
latest_update = filtered_df["last_update"].max()

col1, col2, col3, col4 = st.columns(4)
col1.metric("🏥 Total Trial Sites", f"{total_sites:,}")
col2.metric("📊 Total Trials", f"{total_trials:,}")
col3.metric("🌍 Countries Covered", unique_countries)
col4.metric("🕓 Last Data Update", latest_update)

st.markdown("---")

# ---------------------------------------------------------
# 📈 Charts Section
# ---------------------------------------------------------

# 1️⃣ Top Facilities by Number of Studies
st.subheader("🏆 Top 10 Facilities by Total Studies")
top_facilities = filtered_df.sort_values("trial_count", ascending=False).head(10)
fig1 = px.bar(
    top_facilities,
    x="trial_count",
    y="facility_clean",
    orientation="h",
    color="country",
    color_discrete_sequence=px.colors.qualitative.Set2,
    title="Top Facilities Leading Clinical Trials",
)
st.plotly_chart(fig1, use_container_width=True)

# 2️⃣ Trials by Country
st.subheader("🌍 Trials Distribution by Country")
country_summary = (
    filtered_df.groupby("country")["trial_count"]
    .sum()
    .reset_index()
    .sort_values("trial_count", ascending=False)
)
fig2 = px.choropleth(
    country_summary,
    locations="country",
    locationmode="country names",
    color="trial_count",
    color_continuous_scale="Viridis",
    title="Global Trial Distribution",
)
st.plotly_chart(fig2, use_container_width=True)

# 3️⃣ Status Breakdown (if available)
if "status" in filtered_df.columns:
    st.subheader("📋 Trial Status Breakdown")
    
    # ✅ Compute unique counts safely
    status_counts = (
        filtered_df["status"]
        .value_counts()
        .reset_index(name="count")
        .rename(columns={"index": "status"})
    )

    # ✅ Build the pie chart
    fig3 = px.pie(
        status_counts,
        names="status",
        values="count",
        title="Trial Status Overview",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig3.update_traces(textinfo="percent+label", pull=[0.05]*len(status_counts))

    st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------------
# 📅 Data Table
# ---------------------------------------------------------
st.subheader("🧾 Facility-wise Trial Data")
st.dataframe(
    filtered_df[["facility_clean", "country", "trial_count", "phase", "status", "last_update"]],
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")
st.caption("Built with ❤️ using Streamlit & Plotly · Clinical Trial Insights Dashboard")
