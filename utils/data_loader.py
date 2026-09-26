import os
import pandas as pd
from typing import Dict, Any, Optional
from utils.config import DATASET_DIR, MASTER_DATASET_DIR, OUTPUT_DIR

_DATA_CACHE: Dict[str, pd.DataFrame] = {}

def load_csv_safely(filepath: str | os.PathLike) -> pd.DataFrame:
    """Loads CSV attempting UTF-8 first, falling back to latin-1 / cp1252."""
    try:
        return pd.read_csv(filepath, encoding='utf-8')
    except Exception:
        try:
            return pd.read_csv(filepath, encoding='latin-1')
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return pd.DataFrame()

def get_recommendation_ready_df() -> pd.DataFrame:
    if "rec_ready" not in _DATA_CACHE:
        path = MASTER_DATASET_DIR / "recommendation_ready_dataset.csv"
        df = load_csv_safely(path)
        if df.empty:
            # Fallback to master university dataset
            path = MASTER_DATASET_DIR / "master_university_dataset.csv"
            df = load_csv_safely(path)
        _DATA_CACHE["rec_ready"] = df
    return _DATA_CACHE["rec_ready"].copy()

def get_master_university_df() -> pd.DataFrame:
    if "master_univ" not in _DATA_CACHE:
        path = MASTER_DATASET_DIR / "master_university_dataset.csv"
        _DATA_CACHE["master_univ"] = load_csv_safely(path)
    return _DATA_CACHE["master_univ"].copy()

def get_country_intelligence_df() -> pd.DataFrame:
    if "country_intel" not in _DATA_CACHE:
        path = MASTER_DATASET_DIR / "country_intelligence_dataset.csv"
        _DATA_CACHE["country_intel"] = load_csv_safely(path)
    return _DATA_CACHE["country_intel"].copy()

def get_scholarship_intelligence_df() -> pd.DataFrame:
    if "scholarship_intel" not in _DATA_CACHE:
        path = MASTER_DATASET_DIR / "scholarship_intelligence_dataset.csv"
        df = load_csv_safely(path)
        if df.empty:
            path = DATASET_DIR / "international_scholarships_cleaned.csv"
            df = load_csv_safely(path)
        _DATA_CACHE["scholarship_intel"] = df
    return _DATA_CACHE["scholarship_intel"].copy()

def get_raw_qs_rankings_df() -> pd.DataFrame:
    if "qs_rankings" not in _DATA_CACHE:
        path = DATASET_DIR / "QS World University Rankings 2025 (Top global universities).csv"
        _DATA_CACHE["qs_rankings"] = load_csv_safely(path)
    return _DATA_CACHE["qs_rankings"].copy()

def get_raw_costs_df() -> pd.DataFrame:
    if "costs" not in _DATA_CACHE:
        path = DATASET_DIR / "International_Education_Costs.csv"
        _DATA_CACHE["costs"] = load_csv_safely(path)
    return _DATA_CACHE["costs"].copy()

def get_academic_trends_df() -> pd.DataFrame:
    if "academic" not in _DATA_CACHE:
        path = DATASET_DIR / "academic.csv"
        _DATA_CACHE["academic"] = load_csv_safely(path)
    return _DATA_CACHE["academic"].copy()
