"""Interactive Streamlit dashboard for CogniStream."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "ai_dev_productivity_cleaned.csv"

st.set_page_config(
    page_title="CogniStream Analytics",
    page_icon="🧠",
    layout="wide",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_PATH)
    data["task_outcome"] = data["task_success"].map(
        {0: "Unsuccessful", 1: "Successful"}
    )
    data["cognitive_load_group"] = pd.cut(
        data["cognitive_load"],
        bins=[0, 3, 6, 10],
        labels=["Low (1-3)", "Medium (4-6)", "High (7-10)"],
    )
    return data


df = load_data()

st.title("🧠 CogniStream")
st.subheader("Developer Flow-State & Cognitive Load Analytics")
st.caption(
    "Explore the relationship between work habits, cognitive load and task outcomes. "
    "This dashboard reports associations, not causal conclusions."
)

st.sidebar.header("Filters")
outcomes = st.sidebar.multiselect(
    "Task outcome",
    options=["Successful", "Unsuccessful"],
    default=["Successful", "Unsuccessful"],
)
load_groups = st.sidebar.multiselect(
    "Cognitive-load group",
    options=["Low (1-3)", "Medium (4-6)", "High (7-10)"],
    default=["Low (1-3)", "Medium (4-6)", "High (7-10)"],
)

filtered = df[
    df["task_outcome"].isin(outcomes)
    & df["cognitive_load_group"].astype(str).isin(load_groups)
].copy()

st.markdown("### Executive overview")
metric_columns = st.columns(5)
metric_columns[0].metric("Records", f"{len(filtered):,}")
metric_columns[1].metric(
    "Task success rate",
    f"{filtered['task_success'].mean() * 100:.1f}%" if len(filtered) else "N/A",
)
metric_columns[2].metric(
    "Avg cognitive load",
    f"{filtered['cognitive_load'].mean():.2f}" if len(filtered) else "N/A",
)
metric_columns[3].metric(
    "Avg coding hours",
    f"{filtered['hours_coding'].mean():.2f}" if len(filtered) else "N/A",
)
metric_columns[4].metric(
    "Avg bugs reported",
    f"{filtered['bugs_reported'].mean():.2f}" if len(filtered) else "N/A",
)

if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()

st.markdown("### Task outcomes")
left, right = st.columns(2)
with left:
    outcome_counts = filtered["task_outcome"].value_counts().reindex(
        ["Successful", "Unsuccessful"], fill_value=0
    )
    st.bar_chart(outcome_counts, color=["#1b9e77"])
with right:
    summary = (
        filtered.groupby("cognitive_load_group", observed=False)["task_success"]
        .mean()
        .mul(100)
        .rename("Success rate (%)")
    )
    st.bar_chart(summary, color="#7570b3")

st.markdown("### Productivity and cognitive-load signals")
left, right = st.columns(2)
with left:
    fig, ax = plt.subplots(figsize=(7, 4))
    for label, color in [("Successful", "#1b9e77"), ("Unsuccessful", "#d95f02")]:
        subset = filtered[filtered["task_outcome"] == label]
        ax.scatter(
            subset["hours_coding"],
            subset["cognitive_load"],
            label=label,
            alpha=0.65,
            color=color,
        )
    ax.set_xlabel("Coding hours")
    ax.set_ylabel("Cognitive load")
    ax.set_title("Coding hours vs cognitive load")
    ax.legend()
    st.pyplot(fig, clear_figure=True)
with right:
    group_summary = (
        filtered.groupby("cognitive_load_group", observed=False)
        .agg(
            Success_rate=("task_success", "mean"),
            Average_bugs=("bugs_reported", "mean"),
            Average_distractions=("distractions", "mean"),
        )
        .mul({"Success_rate": 100, "Average_bugs": 1, "Average_distractions": 1})
        .round(2)
    )
    st.dataframe(group_summary, use_container_width=True)

st.markdown("### Selected feature comparison")
feature_options = [
    "hours_coding",
    "sleep_hours",
    "distractions",
    "commits",
    "bugs_reported",
    "ai_usage_hours",
    "cognitive_load",
]
selected_feature = st.selectbox("Choose a feature", feature_options)
feature_summary = (
    filtered.groupby("task_outcome")[selected_feature]
    .mean()
    .reindex(["Successful", "Unsuccessful"])
)
st.bar_chart(feature_summary, color="#1b9e77")

st.markdown("### Data notes")
st.info(
    "The current dataset has no dates, developer IDs or team IDs. "
    "It supports cross-sectional analysis, but not individual trend tracking "
    "or team-level comparisons."
)
