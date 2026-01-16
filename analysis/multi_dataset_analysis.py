import os
import json
import sys
from typing import Dict, List

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio

# Make workspace root importable
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if WORKSPACE_ROOT not in sys.path:
    sys.path.append(WORKSPACE_ROOT)

# Reuse helpers from biometric module
from analysis.biometric_analysis import (
    find_csv_files,
    safe_read_csv,
    coerce_types,
    identify_columns,
    ensure_output_dir,
    outcome_analysis,
)

DATASET_FOLDERS = [
    "api_data_aadhar_enrolment",
    "api_data_aadhar_demographic",
    "api_data_aadhar_biometric",
]

RANDOM_STATE = 42


def save_html(fig, out_dir: str, name: str):
    safe_name = name.replace(" ", "_").replace("/", "-")
    path = os.path.join(out_dir, f"{safe_name}.html")
    pio.write_html(fig, file=path, include_plotlyjs="cdn", auto_open=False)
    return path


def load_dataset(path: str) -> pd.DataFrame:
    files = find_csv_files(path)
    frames = []
    for f in files:
        df = safe_read_csv(f)
        df["__source_file__"] = os.path.basename(f)
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    df_all = pd.concat(frames, ignore_index=True)
    df_all = coerce_types(df_all)
    return df_all


def compute_basic_metrics(df: pd.DataFrame) -> Dict:
    if df.empty:
        return {
            "rows": 0,
            "cols": 0,
            "numeric": 0,
            "categorical": 0,
            "datetime": 0,
            "missing_rate": 1.0,
            "has_label": False,
            "success_rate": None,
            "top_geo": {},
        }
    numeric_cols, datetime_cols, categorical_cols, label_candidates, geo_candidates = identify_columns(df)
    miss_rate = float(df.isna().mean().mean())
    success_rate = None
    has_label = False
    if label_candidates:
        has_label = True
        label = label_candidates[0]
        y = df[label].astype(str).str.lower()
        mapping = {
            "success": 1, "pass": 1, "matched": 1, "true": 1, "1": 1,
            "failure": 0, "fail": 0, "not matched": 0, "false": 0, "0": 0
        }
        y_mapped = y.map(mapping)
        if y_mapped.notna().any():
            success_rate = float(y_mapped.mean())
    top_geo = {}
    for g in geo_candidates[:2]:
        vc = df[g].value_counts(dropna=False).head(10)
        top_geo[g] = vc.to_dict()

    return {
        "rows": int(len(df)),
        "cols": int(df.shape[1]),
        "numeric": len(numeric_cols),
        "categorical": len(categorical_cols),
        "datetime": len(datetime_cols),
        "missing_rate": miss_rate,
        "has_label": has_label,
        "success_rate": success_rate,
        "top_geo": top_geo,
    }


def build_comparative_dashboard(datasets: Dict[str, Dict], workspace_root: str) -> str:
    out_dir = ensure_output_dir(workspace_root, subdir="dashboard")
    # Volumes
    vols = pd.DataFrame([
        {"dataset": k, "rows": v["rows"]} for k, v in datasets.items()
    ])
    fig_vol = px.bar(vols, x="dataset", y="rows", title="Volume by dataset", text="rows")
    save_html(fig_vol, out_dir, "volumes_by_dataset")

    # Missingness
    miss = pd.DataFrame([
        {"dataset": k, "missing_rate": v["missing_rate"]} for k, v in datasets.items()
    ])
    fig_miss = px.bar(miss, x="dataset", y="missing_rate", title="Missingness rate by dataset")
    save_html(fig_miss, out_dir, "missingness_by_dataset")

    # Success rate (if available)
    sr = pd.DataFrame([
        {"dataset": k, "success_rate": v["success_rate"]} for k, v in datasets.items()
        if v.get("success_rate") is not None
    ])
    if not sr.empty:
        fig_sr = px.bar(sr, x="dataset", y="success_rate", title="Outcome success rate by dataset")
        save_html(fig_sr, out_dir, "success_rate_by_dataset")

    # Save a simple index with links
    index_path = os.path.join(out_dir, "index.html")
    with open(index_path, "w", encoding="utf-8") as fh:
        fh.write("""
<!doctype html>
<html>
<head><meta charset='utf-8'><title>Aadhaar Analysis Dashboard</title></head>
<body>
<h1>Aadhaar Analysis Dashboard</h1>
<ul>
  <li><a href='volumes_by_dataset.html'>Volumes by dataset</a></li>
  <li><a href='missingness_by_dataset.html'>Missingness by dataset</a></li>
  <li><a href='success_rate_by_dataset.html'>Success rate by dataset</a></li>
</ul>
<p>See dataset-specific outputs under analysis_outputs/[enrolment|demographic|biometric].</p>
</body>
</html>
""")
    return index_path


def main():
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    results = {}
    for folder in DATASET_FOLDERS:
        path = os.path.join(workspace_root, folder)
        if not os.path.isdir(path):
            continue
        df = load_dataset(path)
        metrics = compute_basic_metrics(df)
        results[folder] = metrics
        # Ensure per-dataset output dir exists
        ensure_output_dir(workspace_root, subdir=folder.replace("api_data_aadhar_", ""))
    dash = build_comparative_dashboard(results, workspace_root)
    print(json.dumps({"dashboard": dash, "datasets": results}, indent=2))


if __name__ == "__main__":
    main()
