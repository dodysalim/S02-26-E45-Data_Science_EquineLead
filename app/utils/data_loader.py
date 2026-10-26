import os
from pathlib import Path
from typing import List

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REQUIRED_DATA_FILES = (
    "horses_listings_limpio.parquet",
    "products_listing_limpio.parquet",
    "horses_sessions_info.parquet",
    "prods_sessions_info.parquet",
    "users_info.parquet",
)


def get_data_directory() -> Path:
    """Support both manual app snapshots and the repository's DVC output."""
    configured = os.getenv("EQUINE_DATA_DIR")
    if configured:
        return Path(configured).expanduser().resolve()
    candidates = [PROJECT_ROOT / "app/data/clean", PROJECT_ROOT / "data/clean"]
    for folder in candidates:
        if all((folder / name).is_file() for name in REQUIRED_DATA_FILES):
            return folder
    for folder in candidates:
        if any((folder / name).is_file() for name in REQUIRED_DATA_FILES):
            return folder
    return candidates[0]


@st.cache_data(show_spinner=False)
def load_data(
    filename: str, cols: List[str] = None, sample_limit: int = None
) -> pd.DataFrame:
    """Optimized data loader with column pruning and cloud-safe engine settings."""
    # Data directory relative to this file
    path = get_data_directory() / filename

    if os.path.exists(path):
        try:
            # Use pyarrow with mmap=False for cloud stability
            df = pd.read_parquet(path, columns=cols, engine="pyarrow", memory_map=False)

            # Universal date conversion
            for date_col in ["first_seen", "event_time", "Birthday"]:
                if date_col in df.columns:
                    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

            # Row capping for performance
            if sample_limit and len(df) > sample_limit:
                df = df.sample(n=sample_limit, random_state=42)

            return df
        except Exception as e:
            st.sidebar.error(f"Error loading {filename}: {e}")
            return pd.DataFrame()
    return pd.DataFrame()


def get_all_dashboard_data():
    """Master orchestrator for data loading with specific column requirements."""
    with st.spinner("Synchronizing Core Engine Data..."):
        df_horses = load_data(
            "horses_listings_limpio.parquet",
            cols=["Breed", "Gender", "Color", "Price", "Age", "Location"],
        )

        df_products = load_data(
            "products_listing_limpio.parquet", cols=["Category", "Price", "Stock"]
        )

        # Ultra-Light Session Loading for Cloud Stability
        try:
            # We use a very small limit (10k) for initial cloud boot to avoid OOM
            df_u_sessions = load_data(
                "horses_sessions_info.parquet",
                cols=["event_time", "event_type", "horse_id"],
                sample_limit=10000,
            )

            df_p_sessions = load_data(
                "prods_sessions_info.parquet",
                cols=["event_time", "event_type", "item_id"],
                sample_limit=10000,
            )
        except Exception as e:
            st.sidebar.error(f"Global Session Engine restricted: {e}")
            df_u_sessions = pd.DataFrame()
            df_p_sessions = pd.DataFrame()

        u_cols = [
            "first_seen",
            "country",
            "city",
            "traffic_source",
            "gender",
            "device_type",
            "job_info",
        ]
        df_users = load_data("users_info.parquet", cols=u_cols)

        # Post-processing for job_info (dictionary extraction)
        if not df_users.empty and "job_info" in df_users.columns:
            df_users["job_info"] = df_users["job_info"].apply(
                lambda x: x.get("title") if isinstance(x, dict) else x
            )

        # Diagnostic for empty sessions (Only if Users/Horses are NOT empty)
        if df_u_sessions.empty and not df_users.empty:
            st.sidebar.info("Note: Horse Session data is empty or filtered.")
        if df_p_sessions.empty and not df_users.empty:
            st.sidebar.info("Note: Product Session data is empty or filtered.")

        return df_horses, df_products, df_users, df_u_sessions, df_p_sessions
