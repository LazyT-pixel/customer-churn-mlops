-- Customer Churn DB schema
-- Ties to COMP214 (Advanced Database Concepts): normalization, keys, views.
--
-- Design note: raw ingested data stays untouched in `raw_customers`.
-- Everything derived (engineered features) lives in a separate table/view,
-- so you can always re-derive features without re-importing source data.
-- This separation is the same reasoning behind normal forms: don't let
-- derived data corrupt or get confused with source-of-truth data.
--
-- Source: telco_churn.csv (IBM Telco Customer Churn, 7,043 rows, 21 columns).

CREATE TABLE IF NOT EXISTS raw_customers (
    customer_id         VARCHAR(20) PRIMARY KEY,
    gender               VARCHAR(10),
    senior_citizen       BOOLEAN,
    partner              BOOLEAN,
    dependents           BOOLEAN,
    tenure_months        INTEGER,
    phone_service        BOOLEAN,
    multiple_lines       VARCHAR(20),   -- "Yes" / "No" / "No phone service"
    internet_service     VARCHAR(20),   -- "DSL" / "Fiber optic" / "No"
    online_security       VARCHAR(20),   -- "Yes" / "No" / "No internet service"
    online_backup        VARCHAR(20),
    device_protection    VARCHAR(20),
    tech_support         VARCHAR(20),
    streaming_tv         VARCHAR(20),
    streaming_movies     VARCHAR(20),
    contract_type        VARCHAR(20),
    paperless_billing    BOOLEAN,
    payment_method       VARCHAR(30),
    monthly_charges      NUMERIC(8,2),
    total_charges        NUMERIC(10,2),  -- nullable, see note below
    churned              BOOLEAN NOT NULL
);

-- Note on `total_charges` being nullable: 11 of 7,043 rows have no valid
-- value in the source CSV -- every one of them is a customer with
-- tenure_months = 0 (confirmed by hand in the REPL: a brand-new customer
-- genuinely has $0 in charges so far). Whether those get imputed to 0 or
-- dropped is a decision made in `load_raw_csv` / `src/data_pipeline.py`,
-- not here -- this table should mirror what the source data actually says.

-- TODO (COMP214): several columns (multiple_lines, internet_service,
-- online_security, online_backup, device_protection, tech_support,
-- streaming_tv, streaming_movies) share a small, repeated set of string
-- values across many rows -- that's a normalization candidate (a lookup
-- table + FK) rather than free text. Pick ONE of them, normalize it
-- properly, and explain in a comment whether it was worth doing for the
-- rest too, or whether that would just add joins for no real benefit at
-- this table size (7,043 rows).

-- TODO (COMP214): add an index that would matter at scale (e.g. on
-- contract_type or tenure_months) and explain in a comment which query
-- pattern it would speed up and why.

-- TODO (COMP214): write a VIEW called `customer_features` that computes
-- at least 2 engineered features via SQL (not pandas), e.g.:
--   - avg_monthly_spend = total_charges / NULLIF(tenure_months, 0)
--   - is_month_to_month = contract_type = 'Month-to-month'
--     (COMP247 note: month-to-month contracts are one of the strongest
--     churn predictors in this dataset -- worth exposing as its own flag
--     rather than making the model infer it from the raw string)
-- This view is the ONLY thing `src/data_pipeline.py` should query for
-- training data -- never raw_customers directly.
