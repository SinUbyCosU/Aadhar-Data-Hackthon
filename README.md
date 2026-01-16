# Aadhaar Data Hackathon Analysis

Advanced analytics and interactive visualizations for enrolment, demographic, and biometric Aadhaar datasets.

## Structure
- `analysis/biometric_analysis.py` — deep-dive analysis + advanced/3D plots (Plotly HTML + PNGs)
- `analysis/multi_dataset_analysis.py` — comparative dashboard across datasets
- `analysis/requirements.txt` — Python dependencies
- Outputs: `analysis_outputs/*`

## Quick Start
```powershell
# Create/activate venv if needed, then install deps
pip install -r analysis/requirements.txt

# Run per-dataset analysis (biometric example)
python analysis/biometric_analysis.py "api_data_aadhar_biometric"

# Build comparative dashboard across all datasets
python analysis/multi_dataset_analysis.py
```

## Notes
- Large CSVs and generated outputs are ignored via `.gitignore`.
- 3D interactive charts are saved as HTML in `analysis_outputs/<dataset>/` and `analysis_outputs/dashboard/`.
