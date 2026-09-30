"""
Data preparation pipeline for the Customer Shopping Behavior project.

Reads the raw CSV, validates it, applies the same transformations that are
implemented in Power Query (powerbi/power_query/transform.m), and writes a
cleaned dataset to data/processed/.

Usage (from the repository root):
    python scripts/data_preparation.py
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "customer_shopping_behavior.csv"
OUT_PATH = ROOT / "data" / "processed" / "customer_shopping_behavior_clean.csv"

FREQUENCY_GROUP = {
    "Weekly": ("Weekly", 1),
    "Bi-Weekly": ("Fortnightly", 2),
    "Fortnightly": ("Fortnightly", 2),
    "Monthly": ("Monthly", 3),
    "Quarterly": ("Quarterly", 4),
    "Every 3 Months": ("Quarterly", 4),
    "Annually": ("Annually", 5),
}
SEASON_SORT = {"Spring": 1, "Summer": 2, "Fall": 3, "Winter": 4}
LOYALTY_BINS = [0, 10, 25, 40, float("inf")]
LOYALTY_LABELS = ["New (1-10)", "Occasional (11-25)", "Regular (26-40)", "Loyal (41+)"]


def validate(df: pd.DataFrame) -> None:
    """Fail loudly if the raw data violates basic expectations."""
    assert df["Customer ID"].is_unique, "Customer ID must be unique"
    assert df["Age"].between(18, 100).all(), "Age out of expected range"
    assert df["Purchase Amount (USD)"].gt(0).all(), "Purchase amount must be positive"
    assert df["Review Rating"].dropna().between(1, 5).all(), "Rating must be 1-5"
    assert set(df["Frequency of Purchases"]) <= set(FREQUENCY_GROUP), "Unknown frequency value"


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Text hygiene
    for col in df.columns[df.dtypes.map(lambda t: not pd.api.types.is_numeric_dtype(t))]:
        df[col] = df[col].str.strip()

    # 'Promo Code Used' is 100% identical to 'Discount Applied' -> redundant
    if (df["Discount Applied"] == df["Promo Code Used"]).all():
        df = df.drop(columns=["Promo Code Used"])

    # Age segments
    df["Age Group"] = pd.cut(
        df["Age"], bins=[17, 25, 35, 45, 55, 120],
        labels=["18-25", "26-35", "36-45", "46-55", "56+"],
    ).astype(str)

    # Purchase value tiers
    df["Purchase Tier"] = pd.cut(
        df["Purchase Amount (USD)"], bins=[0, 39, 79, float("inf")],
        labels=["Low", "Medium", "High"],
    ).astype(str)
    df["Purchase Tier Sort"] = df["Purchase Tier"].map({"Low": 1, "Medium": 2, "High": 3})

    # Loyalty segments from purchase history
    df["Loyalty Segment"] = pd.cut(
        df["Previous Purchases"], bins=LOYALTY_BINS, labels=LOYALTY_LABELS
    ).astype(str)
    df["Loyalty Sort"] = df["Loyalty Segment"].map({l: i + 1 for i, l in enumerate(LOYALTY_LABELS)})

    # Rating bands (missing ratings are kept as 'Not Rated', never imputed)
    band = pd.cut(
        df["Review Rating"], bins=[0, 2.99, 3.99, 5],
        labels=["Low (<3.0)", "Moderate (3.0-3.9)", "High (4.0+)"],
    ).astype(object)
    df["Rating Band"] = band.where(band.notna(), "Not Rated")

    # Standardised purchase frequency (Bi-Weekly == Fortnightly, Quarterly == Every 3 Months)
    df["Frequency Group"] = df["Frequency of Purchases"].map(lambda v: FREQUENCY_GROUP[v][0])
    df["Frequency Sort"] = df["Frequency of Purchases"].map(lambda v: FREQUENCY_GROUP[v][1])

    df["Season Sort"] = df["Season"].map(SEASON_SORT)
    return df


def main() -> None:
    raw = pd.read_csv(RAW_PATH)
    print(f"Loaded {len(raw):,} rows x {raw.shape[1]} columns from {RAW_PATH.name}")
    validate(raw)
    print(f"Missing review ratings: {raw['Review Rating'].isna().sum()} (kept as blank)")

    clean = build_features(raw)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    clean.to_csv(OUT_PATH, index=False)
    print(f"Saved {len(clean):,} rows x {clean.shape[1]} columns -> {OUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
