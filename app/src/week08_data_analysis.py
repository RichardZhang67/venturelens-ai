import pandas as pd

def load_startup_data(file_path: str) -> pd.DataFrame:
    """Load startup dataset from a CSV file."""
    return pd.read_csv(file_path)

def count_by_industry(df: pd.DataFrame) -> pd.Series:
    """Count number of startups in each industry."""
    return df["Industry"].value_counts()

def average_funding_by_industry(df: pd.DataFrame) -> pd.Series:
    """Calculate average funding by industry."""
    return df.groupby("Industry")["Funding"].mean().sort_values(ascending=False)
