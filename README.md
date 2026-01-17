# Aadhaar Data Hackathon Analysis

Advanced analytics and interactive visualizations for enrolment, demographic, and biometric Aadhaar datasets. Includes a national insights summary for quick executive reporting.

## Structure
- `analysis/biometric_analysis.py` — per–dataset deep‑dive analysis with advanced/3D plots (Plotly HTML)
- `analysis/multi_dataset_analysis.py` — comparative dashboard across datasets (volumes, missingness)
- `analysis/generate_insights.py` — aggregates KPIs/state shares/daily throughput and produces `INSIGHTS.md` + JSON
- `analysis/requirements.txt` — Python dependencies
- Data folders: `api_data_aadhar_enrolment/`, `api_data_aadhar_demographic/`, `api_data_aadhar_biometric/`
- Outputs: `analysis_outputs/*` and `INSIGHTS.md`

## Quick Start
```powershell
# 1) Install dependencies (use a venv if preferred)
pip install -r analysis/requirements.txt

# 2) Build comparative dashboard across all datasets
python analysis/multi_dataset_analysis.py

# 3) Generate the national insights report (INSIGHTS.md + insights JSON)
python analysis/generate_insights.py

# Optional: run a per-dataset deep dive (biometric example)
python analysis/biometric_analysis.py "api_data_aadhar_biometric"
```

## Results & Outputs
- Dataset visuals: `analysis_outputs/enrolment`, `analysis_outputs/demographic`, `analysis_outputs/biometric`
- Comparative dashboard: `analysis_outputs/dashboard`
- Insights summary: `INSIGHTS.md` and `analysis_outputs/insights/insights_summary.json`

## Notes
- Large CSVs and generated outputs are ignored via `.gitignore`.
- Interactive charts are saved as HTML and can be opened in a browser.
