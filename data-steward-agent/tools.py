
import json
from pathlib import Path

import pandas as pd
from langchain_core.tools import tool


DATA_FILE = Path(__file__).parent / "clientes.csv"


@tool
def validate_data_quality() -> str:
    """Detect missing values and duplicate records in the customer dataset."""
    df = pd.read_csv(DATA_FILE)

    results = {
        "total_records": len(df),
        "missing_values_by_column": df.isnull().sum().to_dict(),
        "duplicate_records": int(df.duplicated().sum()),
    }

    return json.dumps(results, ensure_ascii=False)


@tool
def get_dataset_statistics() -> str:
    """Calculate descriptive statistics and dataset information."""
    df = pd.read_csv(DATA_FILE)

    results = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "columns": df.columns.tolist(),
        "statistics": df.describe(include="all").fillna("").to_dict(),
    }

    return json.dumps(results, ensure_ascii=False, default=str)
