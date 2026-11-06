"""Clean and validate the CogniStream developer productivity dataset."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


EXPECTED_COLUMNS = [
    "hours_coding",
    "coffee_intake_mg",
    "distractions",
    "sleep_hours",
    "commits",
    "bugs_reported",
    "ai_usage_hours",
    "cognitive_load",
    "task_success",
]

NON_NEGATIVE_COLUMNS = [
    "hours_coding",
    "coffee_intake_mg",
    "distractions",
    "sleep_hours",
    "commits",
    "bugs_reported",
    "ai_usage_hours",
]


def clean_dataset(input_path: Path, output_path: Path) -> pd.DataFrame:
    """Load, validate, clean, and save the dataset."""
    df = pd.read_csv(input_path)
    df.columns = df.columns.str.strip().str.lower()

    missing_columns = sorted(set(EXPECTED_COLUMNS) - set(df.columns))
    if missing_columns:
        raise ValueError(f"Missing expected columns: {missing_columns}")

    df = df[EXPECTED_COLUMNS].copy()
    input_rows = len(df)
    df = df.drop_duplicates().copy()
    duplicate_rows = input_rows - len(df)

    for column in EXPECTED_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    missing_before = int(df.isna().sum().sum())
    rows_before_missing = len(df)
    df = df.dropna(subset=["task_success"]).copy()
    df = df.dropna().copy()
    missing_rows = rows_before_missing - len(df)

    invalid_mask = pd.Series(False, index=df.index)
    for column in NON_NEGATIVE_COLUMNS:
        invalid_mask |= df[column] < 0

    invalid_mask |= ~df["task_success"].isin([0, 1])
    invalid_mask |= ~df["cognitive_load"].between(1, 10)
    invalid_mask |= ~df["sleep_hours"].between(0, 24)
    invalid_mask |= ~df["hours_coding"].between(0, 24)
    invalid_mask |= ~df["ai_usage_hours"].between(0, 24)

    invalid_rows = int(invalid_mask.sum())
    df = df.loc[~invalid_mask].copy()

    integer_columns = [
        "coffee_intake_mg",
        "distractions",
        "commits",
        "bugs_reported",
        "task_success",
    ]
    for column in integer_columns:
        df[column] = df[column].astype("int64")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"Input rows: {input_rows}")
    print(f"Duplicate rows removed: {duplicate_rows}")
    print(f"Missing values found before cleaning: {missing_before}")
    print(f"Rows removed because of missing values: {missing_rows}")
    print(f"Invalid rows removed: {invalid_rows}")
    print(f"Output rows: {len(df)}")
    print(f"Saved cleaned dataset to: {output_path}")
    return df


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/raw/ai_dev_productivity.csv"),
        help="Path to the raw CSV file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed/ai_dev_productivity_cleaned.csv"),
        help="Path for the cleaned CSV file.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    clean_dataset(args.input, args.output)
