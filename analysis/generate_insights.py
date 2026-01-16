import os
import sys
import json
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

# Make workspace root importable
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if WORKSPACE_ROOT not in sys.path:
    sys.path.append(WORKSPACE_ROOT)

from analysis.biometric_analysis import (
    find_csv_files,
    safe_read_csv,
    coerce_types,
    identify_columns,
    ensure_output_dir,
)

DATASET_FOLDERS = [
    ("enrolment", "api_data_aadhar_enrolment"),
    ("demographic", "api_data_aadhar_demographic"),
    ("biometric", "api_data_aadhar_biometric"),
]

RANDOM_STATE = 42


def load_dataset(folder_path: str) -> pd.DataFrame:
    files = find_csv_files(folder_path)
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


def pick_col(cols: List[str], keys: List[str]) -> Optional[str]:
    for c in cols:
        cl = c.lower()
        if any(k in cl for k in keys):
            return c
    return None


def kpis_for_df(df: pd.DataFrame) -> Dict:
    if df.empty:
        return {
            "rows": 0,
            "cols": 0,
            "missing_rate": 1.0,
            "datetime_col": None,
            "date_min": None,
            "date_max": None,
            "state_col": None,
            "district_col": None,
            "n_states": 0,
            "n_districts": 0,
        }
    numeric_cols, datetime_cols, categorical_cols, label_candidates, geo_candidates = identify_columns(df)
    state_col = pick_col(df.columns.tolist(), ["state"])
    district_col = pick_col(df.columns.tolist(), ["district"])
    dt_col = datetime_cols[0] if datetime_cols else None

    miss_rate = float(df.isna().mean().mean())
    dmin = str(df[dt_col].min().date()) if dt_col and df[dt_col].notna().any() else None
    dmax = str(df[dt_col].max().date()) if dt_col and df[dt_col].notna().any() else None

    n_states = int(df[state_col].nunique(dropna=True)) if state_col in df.columns else 0
    n_districts = int(df[district_col].nunique(dropna=True)) if district_col in df.columns else 0

    return {
        "rows": int(len(df)),
        "cols": int(df.shape[1]),
        "missing_rate": miss_rate,
        "datetime_col": dt_col,
        "date_min": dmin,
        "date_max": dmax,
        "state_col": state_col,
        "district_col": district_col,
        "n_states": n_states,
        "n_districts": n_districts,
    }


def state_shares(df: pd.DataFrame, state_col: Optional[str]) -> pd.Series:
    if not state_col or state_col not in df.columns:
        return pd.Series(dtype=float)
    vc = df[state_col].value_counts(dropna=False)
    total = vc.sum()
    if total == 0:
        return pd.Series(dtype=float)
    shares = (vc / total).sort_values(ascending=False)
    shares.name = "share"
    return shares


def daily_volume(df: pd.DataFrame, dt_col: Optional[str]) -> pd.Series:
    if not dt_col or dt_col not in df.columns:
        return pd.Series(dtype=int)
    temp = df[[dt_col]].dropna().copy()
    if temp.empty:
        return pd.Series(dtype=int)
    temp["date"] = temp[dt_col].dt.date
    daily = temp.groupby("date").size()
    daily.name = "count"
    return daily


def write_insights_md(path: str, content: str):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


def render_report(workspace_root: str, results: Dict) -> str:
    out_dir = ensure_output_dir(workspace_root, subdir="insights")
    json_path = os.path.join(out_dir, "insights_summary.json")
    # Build a JSON-serializable snapshot
    serializable = {}
    for ds, data in results.items():
        state_shares = data.get("state_shares")
        if state_shares is not None and not state_shares.empty:
            ss = {str(k): float(v) for k, v in state_shares.items()}
        else:
            ss = {}
        dv = data.get("daily_vol")
        if dv is not None and not dv.empty:
            dv_ser = {str(k): int(v) for k, v in dv.items()}
        else:
            dv_ser = {}
        serializable[ds] = {
            "kpis": data.get("kpis", {}),
            "state_shares": ss,
            "daily_vol": dv_ser,
            "df_cols": data.get("df_cols", []),
        }
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(serializable, fh, indent=2)

    # Build Markdown report
    md = []
    md.append("# National Insights – Aadhaar Data Hackathon\n")

    # Executive Summary
    total_rows = sum(results[d]["kpis"]["rows"] for d in results)
    md.append("## Executive Summary\n")
    md.append(f"- Total records analyzed: {total_rows:,}\n")
    for ds in ["enrolment", "demographic", "biometric"]:
        if ds in results:
            r = results[ds]["kpis"]
            md.append(f"- {ds.title()}: {r['rows']:,} rows, missing rate {r['missing_rate']:.1%} ")
    md.append("\n")

    # Coverage and Gaps
    md.append("## Coverage & Representation Gaps by State\n")
    if all(ds in results and (results[ds]["state_shares"] is not None) and (not results[ds]["state_shares"].empty) for ds in results):
        # Compare shares between datasets
        base = results["enrolment"]["state_shares"] if "enrolment" in results else None
        for ds in ["demographic", "biometric"]:
            if ds in results and base is not None:
                target = results[ds]["state_shares"]
                comp = pd.DataFrame({"enrolment": base, ds: target}).fillna(0.0)
                comp["delta"] = comp[ds] - comp["enrolment"]
                worst = comp.sort_values("delta").head(10)
                md.append(f"### Under-represented in {ds.title()} (vs Enrolment)\n")
                for st, row in worst.iterrows():
                    md.append(f"- {st}: {row[ds]:.2%} vs {row['enrolment']:.2%} (Δ {row['delta']:.2%})")
                md.append("\n")
    else:
        md.append("- State column not detected consistently; skipping share comparison.\n\n")

    # Hotspots
    md.append("## Hotspot States & Districts\n")
    for ds in results:
        k = results[ds]["kpis"]
        md.append(f"### {ds.title()}\n")
        top_states = results[ds]["state_shares"].head(10)
        if not top_states.empty:
            md.append("- Top states by volume share:\n")
            for st, v in top_states.items():
                md.append(f"  - {st}: {v:.2%}")
        else:
            md.append("- State breakdown unavailable.")
        # district top (if present)
        dcol = k.get("district_col")
        if dcol and dcol in results[ds]["df_cols"]:
            # compute district top using stored sample (heavy to recompute)
            pass
        md.append("\n")

    # Throughput & Volatility
    md.append("## Throughput & Volatility (Daily)\n")
    for ds in results:
        dv = results[ds]["daily_vol"]
        if not dv.empty:
            vol = float(dv.std() / max(1.0, dv.mean()))
            md.append(f"- {ds.title()}: volatility (std/mean) = {vol:.2f}, range {dv.index.min()} to {dv.index.max()} ")
        else:
            md.append(f"- {ds.title()}: date column not available; skipping.")
    md.append("\n")

    # Data Quality
    md.append("## Data Quality Priorities\n")
    for ds in results:
        k = results[ds]["kpis"]
        md.append(f"- {ds.title()}: missing rate {k['missing_rate']:.1%}, columns={k['cols']} ")
    md.append("\n")

    # Recommendations
    md.append("## Recommendations (National Scale)\n")
    md.extend([
        "- Expand capacity in top-volume states (e.g., additional mobile centres, extended hours).",
        "- Target under-represented states (negative share deltas) with focused enrolment/biometric drives.",
        "- Reduce missingness in high-impact fields (IDs, timestamps, centre info) to unlock better match rates.",
        "- Monitor daily volatility; staff peak days and smooth demand with appointment slots.",
        "- Instrument operational dashboards per district; set SLAs for data completeness and processing times.",
        "- Add fairness monitoring of success rates across states/centres where labels are available.",
    ])
    md_path = os.path.join(WORKSPACE_ROOT, "INSIGHTS.md")
    write_insights_md(md_path, "\n".join(md) + "\n")
    return md_path


def main():
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    datasets: Dict[str, Dict] = {}
    for key, folder in DATASET_FOLDERS:
        folder_path = os.path.join(workspace_root, folder)
        if not os.path.isdir(folder_path):
            continue
        df = load_dataset(folder_path)
        kpis = kpis_for_df(df)
        states = state_shares(df, kpis.get("state_col")) if kpis.get("state_col") else pd.Series(dtype=float)
        dv = daily_volume(df, kpis.get("datetime_col"))
        datasets[key] = {
            "kpis": kpis,
            "state_shares": states,
            "daily_vol": dv,
            "df_cols": list(df.columns),
        }
    report = render_report(workspace_root, datasets)
    print(json.dumps({"insights": report}, indent=2))


if __name__ == "__main__":
    main()
