import os
import glob
import json
import warnings
from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.ensemble import RandomForestClassifier
import plotly.express as px
import plotly.io as pio

warnings.filterwarnings("ignore", category=UserWarning)

# Config
MAX_SAMPLE_ROWS_LIGHT = 100_000
MAX_SAMPLE_ROWS_HEAVY = 10_000
RANDOM_STATE = 42
PLOT_STYLE = "whitegrid"

sns.set_style(PLOT_STYLE)
plt.rcParams["figure.figsize"] = (12, 6)


def find_csv_files(input_dir: str) -> List[str]:
    files = glob.glob(os.path.join(input_dir, "**", "*.csv"), recursive=True)
    return files


def safe_read_csv(path: str) -> pd.DataFrame:
    # Try common options to handle large/varied CSVs
    for sep in [",", "|", "\t"]:
        try:
            df = pd.read_csv(
                path,
                sep=sep,
                dtype="object",
                low_memory=False,
                encoding="utf-8",
            )
            if df.shape[1] > 1:
                return df
        except Exception:
            pass
    # Fallback
    return pd.read_csv(path, dtype="object", low_memory=False)


def coerce_types(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Try to coerce numeric columns
    for col in df.columns:
        # datetime-like
        if any(k in col.lower() for k in ["date", "time", "dt", "timestamp"]):
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce")
                continue
            except Exception:
                pass
        # numeric-like
        if df[col].dtype == "object":
            # remove common non-numeric chars
            cleaned = (
                df[col]
                .str.replace(",", "", regex=False)
                .str.replace("%", "", regex=False)
                .str.replace(r"[^0-9\.-]", "", regex=True)
            )
            num = pd.to_numeric(cleaned, errors="coerce")
            # if sufficient conversion succeeded, keep numeric
            if num.notna().mean() > 0.5:
                df[col] = num
    return df


def identify_columns(df: pd.DataFrame):
    dtypes = df.dtypes
    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(dtypes[c])]
    datetime_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(dtypes[c])]
    categorical_cols = [
        c
        for c in df.columns
        if c not in numeric_cols + datetime_cols and df[c].nunique(dropna=True) <= 100
    ]
    label_candidates = [
        c
        for c in df.columns
        if any(k in c.lower() for k in [
            "status","result","outcome","verification_status","biometric_status",
            "success","failed","failure","quality_pass","match_result"
        ])
    ]
    geo_candidates = [
        c
        for c in df.columns
        if any(k in c.lower() for k in ["state", "district", "pincode", "pin", "center"])
    ]
    return numeric_cols, datetime_cols, categorical_cols, label_candidates, geo_candidates


def ensure_output_dir(root: str, subdir: str = "biometric") -> str:
    out_dir = os.path.join(root, "analysis_outputs", subdir)
    os.makedirs(out_dir, exist_ok=True)
    return out_dir


def save_plot(out_dir: str, name: str):
    safe_name = name.replace(" ", "_").replace("/", "-")
    path = os.path.join(out_dir, f"{safe_name}.png")
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()
    return path


def save_html(fig, out_dir: str, name: str):
    safe_name = name.replace(" ", "_").replace("/", "-")
    path = os.path.join(out_dir, f"{safe_name}.html")
    pio.write_html(fig, file=path, include_plotlyjs="cdn", auto_open=False)
    return path


def missingness_heatmap(df: pd.DataFrame, out_dir: str):
    sample = df.sample(min(len(df), 5000), random_state=RANDOM_STATE)
    miss = sample.isna().astype(int)
    plt.figure(figsize=(14, 6))
    sns.heatmap(miss.T, cbar=False)
    save_plot(out_dir, "missingness_heatmap")


def correlation_heatmap(df: pd.DataFrame, numeric_cols: List[str], out_dir: str):
    if len(numeric_cols) < 2:
        return
    sample = df[numeric_cols].sample(min(len(df), MAX_SAMPLE_ROWS_LIGHT), random_state=RANDOM_STATE)
    corr = sample.corr(method="spearman")
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr, cmap="coolwarm", center=0)
    save_plot(out_dir, "correlation_heatmap_spearman")


def categorical_distributions(df: pd.DataFrame, categorical_cols: List[str], out_dir: str):
    for col in categorical_cols[:10]:
        vc = df[col].value_counts(dropna=False).head(20)
        plt.figure()
        sns.barplot(x=vc.values, y=vc.index, orient="h")
        plt.title(f"Top categories: {col}")
        save_plot(out_dir, f"categorical_top_{col}")


def numeric_distributions(df: pd.DataFrame, numeric_cols: List[str], out_dir: str):
    for col in numeric_cols[:10]:
        series = df[col].dropna()
        if len(series) == 0:
            continue
        plt.figure()
        sns.histplot(series, bins=50, kde=True)
        plt.title(f"Distribution: {col}")
        save_plot(out_dir, f"distribution_{col}")


def time_series_trends(df: pd.DataFrame, datetime_cols: List[str], out_dir: str):
    if not datetime_cols:
        return
    # Use the first datetime column
    dtc = datetime_cols[0]
    temp = df[[dtc]].dropna().copy()
    if temp.empty:
        return
    temp["date"] = temp[dtc].dt.date
    daily = temp.groupby("date").size()
    plt.figure()
    daily.plot()
    plt.title(f"Daily volume over time: {dtc}")
    save_plot(out_dir, f"time_series_{dtc}")


def geo_analysis(df: pd.DataFrame, geo_candidates: List[str], out_dir: str):
    for col in geo_candidates[:3]:
        vc = df[col].value_counts(dropna=False).head(30)
        plt.figure()
        sns.barplot(x=vc.values, y=vc.index, orient="h")
        plt.title(f"Top geographic units: {col}")
        save_plot(out_dir, f"geo_top_{col}")


def outcome_analysis(df: pd.DataFrame, label_candidates: List[str], out_dir: str):
    if not label_candidates:
        return
    label = label_candidates[0]
    # Try to normalize to binary if possible
    y = df[label].astype(str).str.lower()
    mapping = {
        "success": 1, "pass": 1, "matched": 1, "true": 1, "1": 1,
        "failure": 0, "fail": 0, "not matched": 0, "false": 0, "0": 0
    }
    y_mapped = y.map(mapping)
    if y_mapped.notna().mean() < 0.5:
        # If not binary, show counts only
        vc = y.value_counts(dropna=False).head(15)
        plt.figure()
        sns.barplot(x=vc.values, y=vc.index, orient="h")
        plt.title(f"Outcome distribution: {label}")
        save_plot(out_dir, f"outcome_distribution_{label}")
        return

    df_bin = df.copy()
    df_bin["__label__"] = y_mapped
    # Success rate by top categorical features
    cat_cols = [c for c in df.columns if df[c].dtype == "object" and df[c].nunique(dropna=True) <= 50]
    for col in cat_cols[:5]:
        grp = df_bin.groupby(col)["__label__"].mean().sort_values(ascending=False).head(20)
        plt.figure()
        sns.barplot(x=grp.values, y=grp.index, orient="h")
        plt.title(f"Success rate by {col}")
        save_plot(out_dir, f"success_rate_by_{col}")

    # Feature importance (RandomForest) on numeric features
    num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    if len(num_cols) >= 2 and df_bin["__label__"].notna().sum() > 1_000:
        sample = df_bin[num_cols + ["__label__"]].dropna().sample(
            min(MAX_SAMPLE_ROWS_HEAVY, len(df_bin)), random_state=RANDOM_STATE
        )
        X = sample[num_cols].values
        y = sample["__label__"].values.astype(int)
        rf = RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE, n_jobs=-1)
        rf.fit(X, y)
        importances = pd.Series(rf.feature_importances_, index=num_cols).sort_values(ascending=False).head(20)
        plt.figure()
        sns.barplot(x=importances.values, y=importances.index, orient="h")
        plt.title("Feature importance (RandomForest)")
        save_plot(out_dir, "feature_importance_random_forest")


def pca_and_clustering(df: pd.DataFrame, numeric_cols: List[str], out_dir: str, color_col: Optional[str] = None):
    if len(numeric_cols) < 3:
        return
    sample = df[numeric_cols].dropna().sample(
        min(MAX_SAMPLE_ROWS_HEAVY, len(df)), random_state=RANDOM_STATE
    )
    scaler = StandardScaler()
    X = scaler.fit_transform(sample.values)
    pca = PCA(n_components=2, random_state=RANDOM_STATE)
    Xp = pca.fit_transform(X)

    # KMeans clustering
    best_k, best_score = None, -1
    for k in range(2, 7):
        km = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
        labels = km.fit_predict(X)
        score = silhouette_score(X, labels)
        if score > best_score:
            best_k, best_score = k, score

    km = KMeans(n_clusters=best_k, random_state=RANDOM_STATE, n_init=10)
    clusters = km.fit_predict(X)

    plt.figure()
    palette = sns.color_palette("tab10", n_colors=best_k)
    for i in range(best_k):
        idx = clusters == i
        plt.scatter(Xp[idx, 0], Xp[idx, 1], s=8, alpha=0.7, color=palette[i], label=f"Cluster {i}")
    plt.legend()
    plt.title(f"PCA (2D) with KMeans (k={best_k}, silhouette={best_score:.2f})")
    save_plot(out_dir, "pca_kmeans_clusters")


def pca_3d_plot(df: pd.DataFrame, numeric_cols: List[str], out_dir: str, label_candidates: List[str]):
    if len(numeric_cols) < 3:
        return
    sample = df[numeric_cols].dropna().sample(
        min(MAX_SAMPLE_ROWS_HEAVY, len(df)), random_state=RANDOM_STATE
    )
    scaler = StandardScaler()
    X = scaler.fit_transform(sample.values)
    pca = PCA(n_components=3, random_state=RANDOM_STATE)
    Xp = pca.fit_transform(X)
    plot_df = pd.DataFrame({
        "PC1": Xp[:, 0], "PC2": Xp[:, 1], "PC3": Xp[:, 2]
    })

    color_col = None
    if label_candidates:
        # Use first label candidate for color encoding
        color_col = label_candidates[0]
        plot_df[color_col] = df.loc[sample.index, color_col].astype(str)

    fig = px.scatter_3d(
        plot_df,
        x="PC1", y="PC2", z="PC3",
        color=color_col if color_col else None,
        opacity=0.7,
        title="PCA (3D) projection"
    )
    save_html(fig, out_dir, "pca_3d_projection")


def top3_corr_3d_scatter(df: pd.DataFrame, numeric_cols: List[str], out_dir: str):
    if len(numeric_cols) < 3:
        return
    corr = df[numeric_cols].corr(method="spearman").abs()
    # Find top correlated pair
    corr_vals = corr.where(~np.eye(corr.shape[0], dtype=bool))
    max_pair = corr_vals.stack().idxmax()  # (c1, c2)
    c1, c2 = max_pair
    remaining = [c for c in numeric_cols if c not in [c1, c2]]
    if not remaining:
        return
    # Choose third with highest correlation to either c1 or c2
    c3 = max(remaining, key=lambda c: max(corr.loc[c, c1], corr.loc[c, c2]))
    tri = [c1, c2, c3]
    sample = df[tri].dropna().sample(
        min(MAX_SAMPLE_ROWS_HEAVY, len(df)), random_state=RANDOM_STATE
    )
    fig = px.scatter_3d(sample, x=c1, y=c2, z=c3, opacity=0.7,
                        title=f"3D scatter of top-correlated trio: {c1}, {c2}, {c3}")
    save_html(fig, out_dir, "top3_corr_3d_scatter")


def analyze_folder(input_dir: str, workspace_root: str):
    csvs = find_csv_files(input_dir)
    if not csvs:
        raise FileNotFoundError(f"No CSVs found in {input_dir}")

    frames = []
    for f in csvs:
        df = safe_read_csv(f)
        df["__source_file__"] = os.path.basename(f)
        frames.append(df)

    df_all = pd.concat(frames, ignore_index=True)
    df_all = coerce_types(df_all)

    out_dir = ensure_output_dir(workspace_root, subdir="biometric")

    # Persist basic schema report
    report = {
        "rows": int(len(df_all)),
        "cols": int(df_all.shape[1]),
        "dtypes": {c: str(dt) for c, dt in df_all.dtypes.items()},
        "sample_files": list({df_all["__source_file__"].iloc[i] for i in range(min(5, len(df_all)))})
    }
    with open(os.path.join(out_dir, "schema_report.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)

    # Identify columns
    numeric_cols, datetime_cols, categorical_cols, label_candidates, geo_candidates = identify_columns(df_all)

    # Plots
    missingness_heatmap(df_all, out_dir)
    correlation_heatmap(df_all, numeric_cols, out_dir)
    categorical_distributions(df_all, categorical_cols, out_dir)
    numeric_distributions(df_all, numeric_cols, out_dir)
    time_series_trends(df_all, datetime_cols, out_dir)
    geo_analysis(df_all, geo_candidates, out_dir)
    outcome_analysis(df_all, label_candidates, out_dir)

    # PCA + clustering (advanced structure insight)
    color_col = label_candidates[0] if label_candidates else None
    pca_and_clustering(df_all, numeric_cols, out_dir, color_col=color_col)
    # 3D plots
    pca_3d_plot(df_all, numeric_cols, out_dir, label_candidates)
    top3_corr_3d_scatter(df_all, numeric_cols, out_dir)

    return out_dir


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Advanced biometric CSV analysis and plotting")
    parser.add_argument("input_dir", help="Folder containing biometric CSV files")
    parser.add_argument("--workspace_root", default=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    args = parser.parse_args()

    out_dir = analyze_folder(args.input_dir, args.workspace_root)
    print(json.dumps({"outputs": out_dir}, indent=2))


if __name__ == "__main__":
    main()
