# Customer Churn Prediction — End-to-End ML System

A supervised learning project built with production practices, not just a notebook.
This ties together three of my current courses: database design (COMP214), supervised
learning (COMP247), and ML testing / MLOps (COMP315).

## What this is

A binary classification system that predicts whether a customer will churn, built the
way a real ML team would build it: data lives in a relational database with a real
schema, the model is trained through a script (not a notebook you run once and forget),
and every change is checked by automated tests before it's trusted.

## Why it exists

Proving I can do the full pipeline, not just fit a model in a notebook and stop.
Anyone can call `.fit()`. Fewer people can explain why their features are valid, prove
their model doesn't silently regress, and hand off a system someone else could run.

## Architecture

```
Raw CSV  -->  PostgreSQL (raw + feature tables)  -->  Feature engineering (SQL views)
          -->  Training script  -->  Serialized model + metrics report
          -->  Test suite (data validation + model performance gates)
          -->  CI (GitHub Actions) runs tests on every push
```

## Project structure

```
sql/                  schema + feature engineering views
src/
  data_pipeline.py     load CSV -> Postgres, run feature queries
  train.py             train + evaluate + serialize the model
  model.py             model definition / wrapper
tests/
  test_data_validation.py    schema + data quality checks
  test_model_performance.py  performance regression gate
.github/workflows/ci.yml     runs the test suite on every push
```

## Status

Early scaffold. See TODOs in each file — intentionally not solved for you.

## Dataset

IBM Telco Customer Churn (7,043 customers, 21 columns): demographics, account
info (contract type, payment method, tenure), the services each customer is
subscribed to, and monthly/total charges. ~26.5% churn rate (1,869 of 7,043).
Real messiness worth knowing about: `TotalCharges` reads in as a string, not a
number — 11 rows have a blank value instead of 0, all of them customers with
0 months of tenure (confirmed by hand, not assumed).

## Setup

```bash
uv python install 3.11
uv venv --python 3.11 venv
source venv/Scripts/activate   # Windows Git Bash
uv pip install -r requirements.txt
```

## Running tests

```bash
pytest tests/ -v
```

## Author

Aidan Williams

## License

MIT — see [LICENSE](LICENSE).
=======
# customer-churn-mlops
A supervised learning project built with production practices, not just a notebook. This ties together three of my current courses: database design (COMP214), supervised learning (COMP247), and ML testing / MLOps (COMP315).