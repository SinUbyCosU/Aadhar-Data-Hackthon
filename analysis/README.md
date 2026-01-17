# Aadhaar CSV Analysis (Per‑Dataset)

This toolkit loads all CSVs in a selected dataset folder and produces advanced, non‑basic plots and insights.

## Quick Start

1. Ensure Python 3.9+ is available.
2. Install dependencies:

```
pip install -r analysis/requirements.txt
```

3. Run the analysis for the biometric dataset:

```
python analysis/biometric_analysis.py "api_data_aadhar_biometric"
```

Outputs will be saved under `analysis_outputs/biometric`.

## What You Get
- Missingness heatmap (data quality)
- Spearman correlation heatmap (numeric relationships)
- Top categorical distributions (operational mix)
- Numeric distributions (skew/outliers)
- Time series trend (if date-like columns exist)
- Geographic breakdown (state/district/pincode/center if present)
- Outcome analysis and success rates (if outcome-like column exists)
- PCA + KMeans clustering to surface latent structure
- RandomForest feature importance (if binary outcome is detected)

## Other Tools
- Comparative dashboards across datasets: `analysis/multi_dataset_analysis.py`
- National insights summary (produces `INSIGHTS.md` + JSON): `analysis/generate_insights.py`

## Notes
- Handles multi-file folders and mixed CSV formats automatically.
- Samples large data for heavy computations to keep runtime reasonable.
