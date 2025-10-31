🧬 Clinical Trials Report Generator

An intelligent data pipeline and dashboard for exploring clinical trial site performance.
It fetches real-world data from the ClinicalTrials.gov API, cleans and aggregates it by facility, computes trial activity scores, and visualizes insights using Streamlit.

🚀 Features

✅ Automated Data Extraction
Fetches real trial data using the official ClinicalTrials.gov API v2
.

✅ Smart Data Cleaning & Aggregation
Normalizes facility names, merges duplicate entries, and groups by site and country.

✅ Site Analytics
Generates site-wise summaries including:

Total trials (trial_count)

Active phases

Conditions studied

Completion rate and last update

✅ Scoring System
Computes:

Match Score → How relevant a site is to a target condition, phase, and country

Data Quality Score → How consistent and recent its data is

✅ Streamlit Dashboard
Visualize and filter sites interactively by:

Country

Condition

Match score

Data freshness

🧩 Project Structure
Clinical-Trials-Report-Generator/
│
├── extract.py          # Fetches trial data from ClinicalTrials.gov API
├── transform.py        # Cleans, flattens, and aggregates trial data
├── analyze.py          # Summarizes sites and calculates completion metrics
├── score.py            # Contains match_score and data_quality logic
├── database.py         # Saves results to SQLite database
├── main.py             # Main ETL + scoring pipeline
├── app.py              # Streamlit dashboard interface
├── clinical_summary.csv # Exported analytics CSV
├── clinical_trials.db   # SQLite database (generated after first run)
└── README.md            # Project documentation

⚙️ Setup Instructions
1️⃣ Clone the Repository
git clone https://github.com/yourusername/Clinical-Trials-Report-Generator.git
cd Clinical-Trials-Report-Generator

2️⃣ Create a Virtual Environment
python -m venv venv
venv\Scripts\activate      # on Windows
source venv/bin/activate   # on macOS/Linux

3️⃣ Install Dependencies
pip install -r requirements.txt


(If you don’t have requirements.txt, install manually)

pip install pandas requests streamlit matplotlib

🧠 Run the Pipeline
python main.py


This script will:

Fetch 1000 latest trials (default filter: condition="cancer", phase="3")

Aggregate and score site performance

Save results into:

clinical_trials.db

clinical_summary.csv

🌐 Launch Streamlit Dashboard
python -m streamlit run app.py


After initialization, open your browser and visit:

http://localhost:8501


You’ll see:

A searchable site list

Country/phase filters

Charts for top performing facilities

Match & data quality heatmaps

📊 Example Output
Facility Name	Country	Trial Count	Conditions	Match Score	Data Quality
Tata Memorial Hospital	India	12	Cancer, Leukemia	0.89	0.95
Johns Hopkins Hospital	USA	8	Lung Cancer	0.76	0.88
AIIMS New Delhi	India	5	Breast Cancer	0.72	0.83
🧱 Future Improvements

Add trend visualization by year (from last_update field)

Enable multi-condition search

Integrate map visualization using pydeck

Automate daily ETL runs with GitHub Actions

You’re free to use, modify, and distribute this project for learning or research purposes.