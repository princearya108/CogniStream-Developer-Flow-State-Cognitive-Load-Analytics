"""Generate reproducible EDA tables and charts for the CogniStream project."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "ai_dev_productivity_cleaned.csv"
OUTPUT_DIR = ROOT / "outputs" / "eda"

sns.set_theme(style="whitegrid", palette="deep")


def save_plot(filename: str) -> None:
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename, dpi=160, bbox_inches="tight")
    plt.close()


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_PATH)

    quality = pd.DataFrame(
        {
            "rows": [len(df)],
            "columns": [df.shape[1]],
            "duplicate_rows": [int(df.duplicated().sum())],
            "missing_cells": [int(df.isna().sum().sum())],
        }
    )
    quality.to_csv(OUTPUT_DIR / "data_quality_summary.csv", index=False)
    df.describe().T.to_csv(OUTPUT_DIR / "descriptive_statistics.csv")

    success_summary = (
        df.groupby("task_success")
        .agg(
            records=("task_success", "size"),
            success_rate=("task_success", "mean"),
            avg_coding_hours=("hours_coding", "mean"),
            avg_sleep_hours=("sleep_hours", "mean"),
            avg_distractions=("distractions", "mean"),
            avg_commits=("commits", "mean"),
            avg_bugs=("bugs_reported", "mean"),
            avg_ai_usage_hours=("ai_usage_hours", "mean"),
            avg_cognitive_load=("cognitive_load", "mean"),
        )
        .reset_index()
    )
    success_summary["task_success_label"] = success_summary["task_success"].map(
        {0: "Unsuccessful", 1: "Successful"}
    )
    success_summary.to_csv(OUTPUT_DIR / "success_group_summary.csv", index=False)

    cognitive_summary = (
        df.assign(
            cognitive_load_group=pd.cut(
                df["cognitive_load"],
                bins=[0, 3, 6, 10],
                labels=["Low (1-3)", "Medium (4-6)", "High (7-10)"],
            )
        )
        .groupby("cognitive_load_group", observed=False)
        .agg(
            records=("task_success", "size"),
            task_success_rate=("task_success", "mean"),
            avg_bugs=("bugs_reported", "mean"),
            avg_distractions=("distractions", "mean"),
            avg_coding_hours=("hours_coding", "mean"),
        )
        .reset_index()
    )
    cognitive_summary.to_csv(OUTPUT_DIR / "cognitive_load_summary.csv", index=False)

    plt.figure(figsize=(7, 5))
    sns.countplot(data=df, x="task_success", hue="task_success", legend=False)
    plt.xticks([0, 1], ["Unsuccessful", "Successful"])
    plt.xlabel("Task outcome")
    plt.ylabel("Number of records")
    plt.title("Task Success Balance")
    save_plot("01_task_success_balance.png")

    features = ["hours_coding", "sleep_hours", "distractions", "cognitive_load"]
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    for ax, feature in zip(axes.flat, features):
        sns.histplot(data=df, x=feature, hue="task_success", kde=True, ax=ax)
        ax.set_title(f"{feature.replace('_', ' ').title()} Distribution")
    save_plot("02_feature_distributions.png")

    plot_features = [
        "hours_coding",
        "sleep_hours",
        "distractions",
        "commits",
        "bugs_reported",
        "ai_usage_hours",
        "cognitive_load",
    ]
    long_df = df.melt(
        id_vars="task_success",
        value_vars=plot_features,
        var_name="feature",
        value_name="value",
    )
    plt.figure(figsize=(13, 6))
    sns.boxplot(data=long_df, x="feature", y="value", hue="task_success")
    plt.xticks(rotation=35, ha="right")
    plt.title("Feature Values by Task Outcome")
    plt.xlabel("")
    plt.ylabel("Value")
    save_plot("03_features_by_task_outcome.png")

    plt.figure(figsize=(8, 5))
    sns.barplot(
        data=success_summary,
        x="task_success_label",
        y="avg_cognitive_load",
        hue="task_success_label",
        legend=False,
    )
    plt.title("Average Cognitive Load by Task Outcome")
    plt.xlabel("")
    plt.ylabel("Average cognitive load")
    save_plot("04_cognitive_load_by_outcome.png")

    plt.figure(figsize=(8, 5))
    sns.barplot(
        data=cognitive_summary,
        x="cognitive_load_group",
        y="task_success_rate",
        hue="cognitive_load_group",
        legend=False,
    )
    plt.ylim(0, 1)
    plt.title("Task Success Rate by Cognitive Load Group")
    plt.xlabel("")
    plt.ylabel("Task success rate")
    save_plot("05_success_by_cognitive_load.png")

    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(numeric_only=True), annot=True, fmt=".2f", cmap="vlag", center=0)
    plt.title("Correlation Matrix")
    save_plot("06_correlation_heatmap.png")

    print(f"Loaded {len(df):,} records")
    print(f"Output directory: {OUTPUT_DIR}")
    print(success_summary.to_string(index=False))
    print(cognitive_summary.to_string(index=False))


if __name__ == "__main__":
    main()
