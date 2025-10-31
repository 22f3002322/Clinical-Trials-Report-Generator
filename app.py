import streamlit as st
import pandas as pd
import subprocess
from analyze import summarize_sites
from database import load_from_db, load_latest_metadata
import plotly.express as px

st.set_page_config(page_title="Clinical Trial Site Intelligence", layout="wide")

st.title("🏥 Clinical Trial Site Intelligence Dashboard")

# ======================================================
# 🔄 Sidebar — fetch new data
# ======================================================
st.sidebar.header("🔄 Update / Fetch New Data")

cond_input = st.sidebar.text_input("Enter condition (e.g., lung cancer)", "cancer")
phase_input = st.sidebar.selectbox("Select Phase", ["1", "2", "3"])
max_results = st.sidebar.slider("Max Trials to Fetch", 100, 2000, 1000, step=100)

if st.sidebar.button("Fetch New Data"):
    with st.spinner(f"Fetching new {cond_input} (Phase {phase_input}) data..."):
        try:
            subprocess.run(
                [
                    "python",
                    "main.py",
                    "--condition", cond_input,
                    "--phase", phase_input,
                ],
                check=True,
            )
            st.success(f"✅ Database updated for {cond_input} (Phase {phase_input})!")
            st.cache_data.clear()
        except Exception as e:
            st.error(f"❌ Error while fetching data: {e}")

st.sidebar.markdown("---")
st.sidebar.caption("💡 Tip: Try 'breast cancer', 'lung cancer', 'diabetes', etc.")

# ======================================================
# 🧠 Show Last Fetched Info
# ======================================================
meta = load_latest_metadata()
if meta:
    st.markdown(f"""
    **🧠 Last Fetched Data**
    - Condition: `{meta['condition']}`
    - Phase: `{meta['phase']}`
    - Updated: `{meta['updated_at']}`
    """)
else:
    st.info("No previous fetch found. Use sidebar to fetch first dataset.")

# ======================================================
# 📊 Load and display current summary
# ======================================================
st.subheader("📋 Current Summary")

@st.cache_data
def load_summary():
    try:
        df = load_from_db()
        return summarize_sites(df)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

summary = load_summary()

if summary.empty:
    st.warning("No data available. Try fetching new data from the sidebar.")
else:
    # ======================================================
    # 🔢 Top Facilities by Match Score
    # ======================================================
    st.subheader("🏆 Top Facilities by Match Score")
    top_sites = summary.sort_values(by="match_score", ascending=False).head(20)

    fig_rank = px.bar(
        top_sites,
        x="facility_clean",
        y="match_score",
        color="country",
        title="Match Score Ranking",
        labels={"facility_clean": "Facility", "match_score": "Match Score"},
    )
    st.plotly_chart(fig_rank, use_container_width=True)

    # ======================================================
    # 🌍 Trials per Country
    # ======================================================
    st.subheader("🌍 Trials per Country")
    fig_country = px.bar(
        summary.groupby("country")["nct_id"].count().reset_index().rename(columns={"nct_id": "trial_count"}),
        x="country",
        y="trial_count",
        title="Number of Trials by Country",
    )
    st.plotly_chart(fig_country, use_container_width=True)

    # ======================================================
    # 📈 Match Score vs Data Quality
    # ======================================================
    st.subheader("📈 Match Score vs Data Quality")
    fig_scatter = px.scatter(
        summary,
        x="match_score",
        y="data_quality",
        color="country",
        hover_data=["facility_clean", "trial_count"],
        title="Match Score vs Data Quality",
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # ======================================================
    # 📑 Data Table
    # ======================================================
    st.subheader("📑 Data Table")
    st.dataframe(summary.head(50))

    st.success("✅ Dashboard loaded successfully!")
