import streamlit as st
import pandas as pd
import subprocess
import sqlite3
import plotly.express as px
import os
from datetime import datetime

DB_PATH = "clinical_trials.db"

# -------------------------
# Database utilities
# -------------------------
def load_summary():
    if not os.path.exists(DB_PATH):
        st.warning("No database found. Please run the pipeline first.")
        return None

    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql("SELECT * FROM site_analysis", conn)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        conn.close()
        return None
    conn.close()
    return df


def load_metadata():
    conn = sqlite3.connect(DB_PATH)
    try:
        meta = pd.read_sql("SELECT * FROM metadata ORDER BY timestamp DESC LIMIT 1", conn)
    except Exception:
        meta = pd.DataFrame()
    conn.close()
    return meta


# -------------------------
# Sidebar Controls
# -------------------------
st.sidebar.title("⚙️ Pipeline Controls")

condition = st.sidebar.text_input("Condition", "cancer")
phase = st.sidebar.selectbox("Trial Phase", ["1", "2", "3"], index=2)
max_results = st.sidebar.slider("Max Results", 100, 2000, 1000, step=100)

if st.sidebar.button("🚀 Fetch & Process Data"):
    with st.spinner(f"Running pipeline for {condition} (Phase {phase})..."):
        try:
            subprocess.run(
                ["python", "main.py", "--condition", condition, "--phase", phase, "--max_results", str(max_results)],
                check=True,
                capture_output=True,
                text=True,
            )
            st.success("✅ Pipeline completed successfully!")
        except subprocess.CalledProcessError as e:
            st.error(f"❌ Error while fetching data: {e}")
            st.text(e.output)

# -------------------------
# Main Dashboard
# -------------------------
st.title("🏥 Clinical Trial Site Analysis Dashboard")

metadata = load_metadata()
if not metadata.empty:
    m = metadata.iloc[0]
    st.info(f"""
    **🧠 Last Fetched Data**  
    **Condition:** {m['condition']}  
    **Phase:** {m['phase']}  
    **Updated:** {m['timestamp']}
    """)

summary = load_summary()
if summary is None or summary.empty:
    st.warning("No data available. Try fetching new data from the sidebar.")
    st.stop()

# -------------------------
# Data Cleanup
# -------------------------
if "trial_count" not in summary.columns and "nct_id" in summary.columns:
    summary["trial_count"] = summary["nct_id"].apply(
        lambda x: len(x.split(",")) if isinstance(x, str) else 0
    )

# Handle missing match_score gracefully
if "match_score" not in summary.columns:
    summary["match_score"] = 0

# -------------------------
# Charts Section
# -------------------------
st.subheader("🏆 Top Sites by Match Score")

top_sites = summary.sort_values(by="match_score", ascending=False).head(20)
fig1 = px.bar(
    top_sites,
    x="facility_clean",
    y="match_score",
    color="country",
    text="trial_count",
    title="Top 20 Facilities by Match Score",
)
fig1.update_layout(xaxis_title="Facility", yaxis_title="Match Score", xaxis_tickangle=-45)
st.plotly_chart(fig1, use_container_width=True)

# -------------------------
# Trials by Country
# -------------------------
st.subheader("🌍 Trials by Country")

country_summary = (
    summary.groupby("country")["trial_count"].sum().reset_index().sort_values("trial_count", ascending=False)
)
fig2 = px.bar(country_summary, x="country", y="trial_count", title="Total Trials by Country")
st.plotly_chart(fig2, use_container_width=True)

# Optional: Map visualization (if city data available)
if "country" in summary.columns:
    st.subheader("🗺️ Geographic Distribution")
    country_counts = (
        summary.groupby("country")["trial_count"].sum().reset_index()
    )
    fig_map = px.choropleth(
        country_counts,
        locations="country",
        locationmode="country names",
        color="trial_count",
        color_continuous_scale="Blues",
        title="Clinical Trials by Country",
    )
    st.plotly_chart(fig_map, use_container_width=True)

# -------------------------
# Raw Data
# -------------------------
st.subheader("📋 Full Data")
st.dataframe(summary)

st.success("✅ Dashboard loaded successfully!")
