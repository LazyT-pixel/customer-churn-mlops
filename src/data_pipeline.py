"""
Data pipeline: raw CSV -> Postgres -> engineered features.

This is a skeleton. Fill in the TODOs. Don't just make it run -- make it
correct: think about what happens on a re-run (should loading twice
duplicate rows?), and what happens on bad input (a row with a null
`total_charges`, a numeric column that failed to parse).
"""
from sqlalchemy import create_engine
import pandas as pd
import os

DB_URL = os.environ.get("CHURN_DB_URL", "postgresql://localhost/churn_db")

# Column names as they appear in the raw CSV, mapped to the snake_case
# names used in `raw_customers` (sql/schema.sql). Keeping this mapping
# explicit and in one place means if the source file's headers ever
# change, there's exactly one line to fix -- not a search through every
# function that touches a column name.
COLUMN_MAP = {
    "customerID": "customer_id",
    "gender": "gender",
    "SeniorCitizen": "senior_citizen",
    "Partner": "partner",
    "Dependents": "dependents",
    "tenure": "tenure_months",
    "PhoneService": "phone_service",
    "MultipleLines": "multiple_lines",
    "InternetService": "internet_service",
    "OnlineSecurity": "online_security",
    "OnlineBackup": "online_backup",
    "DeviceProtection": "device_protection",
    "TechSupport": "tech_support",
    "StreamingTV": "streaming_tv",
    "StreamingMovies": "streaming_movies",
    "Contract": "contract_type",
    "PaperlessBilling": "paperless_billing",
    "PaymentMethod": "payment_method",
    "MonthlyCharges": "monthly_charges",
    "TotalCharges": "total_charges",
    "Churn": "churned",
}


def load_raw_csv(csv_path: str) -> pd.DataFrame:

    df = pd.read_csv(csv_path)
    df = df.rename(columns=COLUMN_MAP)
    df["total_charges"] = pd.to_numeric(df["total_charges"], errors="coerce")
    df = df[df["total_charges"].notna()]


    """Load the raw IBM Telco churn CSV into a DataFrame, cleaned and
    rename-mapped to match `raw_customers` in sql/schema.sql.

    TODO, in order -- do them in this order, each one depends on the last:

    1. Read the CSV, rename columns using COLUMN_MAP above.

    2. `TotalCharges` reads in as StringDtype, not numeric. You already
       worked out why in the REPL: 11 rows have a blank value instead of
       a number, and every one of them is a customer with tenure == 0 --
       a brand-new customer genuinely has $0 in total charges so far.
       Convert the column to numeric with pd.to_numeric(..., errors="coerce"),
       then decide: impute those 11 as 0 (defensible -- you know exactly
       why they're blank), or drop them (also defensible -- 11 of 7,043
       is 0.16% of the data, small enough not to matter either way). Pick
       one, and write the one-line reason in a comment next to the code,
       not just in your head.

    3. `gender`, `Partner`, `Dependents`, `PhoneService`, `PaperlessBilling`,
       and `churned` (source column "Churn") all come in as "Yes"/"No" or
       similar Yes/No-style strings. Convert the true binary ones (Partner,
       Dependents, PhoneService, PaperlessBilling, churned) to real
       booleans. `gender` is Male/Female -- decide whether that belongs as
       a boolean or should stay categorical (it's not really a yes/no
       concept, forcing it into a bool would be a modeling choice, not a
       cleaning one -- leave it as a string here and make that decision
       later in feature engineering, not in this function).

    4. `MultipleLines`, `InternetService`, `OnlineSecurity`, `OnlineBackup`,
       `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`
       aren't plain Yes/No -- they include values like "No internet
       service". Look at `df[col].unique()` for each one before deciding
       how to encode it. Collapsing "No" and "No internet service" into
       the same boolean False might be right, or it might be throwing away
       a real signal (a customer without internet service structurally
       can't churn on an internet-dependent complaint). Decide, and again,
       write down why.

    5. Return the cleaned, renamed DataFrame -- don't write to the DB here,
       that's write_to_db's job. Keep these functions doing one thing each.
    """
    raise NotImplementedError("TODO: implement CSV loading + cleaning")


def write_to_db(df: pd.DataFrame, table_name: str = "raw_customers") -> None:
    """Write a cleaned DataFrame to Postgres.

    TODO: use `if_exists="replace"` for now during development, but leave
    a comment explaining why that would be wrong in a real production
    pipeline (hint: what if the table has downstream consumers, indexes,
    or you want incremental loads instead of full reloads?).
    """
    raise NotImplementedError("TODO: implement DB write via sqlalchemy engine")


def get_feature_table() -> pd.DataFrame:
    """Query the `customer_features` view (see sql/schema.sql) and return
    it as a DataFrame ready for training.

    TODO: implement. This should be the ONLY place `train.py` reads
    features from -- train.py should never touch raw_customers directly.
    """
    raise NotImplementedError("TODO: implement feature query")


if __name__ == "__main__":
    # TODO: wire these three functions together into a runnable script:
    # load_raw_csv -> write_to_db -> (run schema.sql to create the view,
    # by hand or via psql) -> get_feature_table() to sanity check it works.
    pass
