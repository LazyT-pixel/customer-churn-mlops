"""
Data validation tests -- COMP315 territory.

The idea: before you ever train a model, you should be able to prove your
data meets the assumptions the rest of the pipeline depends on. If someone
(including future-you) changes the raw CSV or the DB schema, these tests
should fail loudly instead of letting a silently-corrupted dataset train a
model that looks fine but is garbage.

One example is fully implemented below so you can see the pattern. The rest
are your job -- write them the same way: arrange a small fixture, assert
something that MUST be true, and give the assertion message enough context
that a failure tells you what broke without needing to re-read the test.
"""
import pandas as pd
import pytest


@pytest.fixture
def sample_customers():
    """A tiny, hand-built fixture -- NOT the real dataset. Clean by design:
    this is what "good" data looks like, so the suite is green by default.
    """
    return pd.DataFrame([
        {"customer_id": "A1", "tenure_months": 12, "monthly_charges": 70.5, "churned": False},
        {"customer_id": "A2", "tenure_months": 0,  "monthly_charges": 20.0, "churned": True},
        {"customer_id": "A3", "tenure_months": 5,  "monthly_charges": 55.0, "churned": False},
    ])


@pytest.fixture
def corrupted_customers(sample_customers):
    """Same shape as sample_customers, but with one bad row injected --
    used below to prove the validation test actually catches something,
    instead of just trusting that it would.
    """
    bad_row = pd.DataFrame([
        {"customer_id": "A4", "tenure_months": -3, "monthly_charges": 55.0, "churned": False},
    ])
    return pd.concat([sample_customers, bad_row], ignore_index=True)


def test_tenure_is_non_negative(sample_customers):
    """tenure_months should never be negative -- it's a count of months.
    A negative value here means an upstream bug, not a valid customer.
    """
    bad_rows = sample_customers[sample_customers["tenure_months"] < 0]
    assert bad_rows.empty, (
        f"Found {len(bad_rows)} row(s) with negative tenure_months: "
        f"{bad_rows['customer_id'].tolist()}"
    )


def test_no_duplicate_customer_ids(sample_customers):
    """customer_id is the primary key -- duplicates mean the load step
    is broken (e.g. re-running the pipeline appended instead of upserting).
    """
    dupes = sample_customers["customer_id"].duplicated()
    assert not dupes.any(), f"Duplicate customer_id(s) found: {sample_customers[dupes]['customer_id'].tolist()}"


def test_churned_is_boolean(sample_customers):
    """churned must be strictly boolean -- not 'Yes'/'No' strings that
    happened to survive a bad cast somewhere in the pipeline.
    """
    assert sample_customers["churned"].dtype == bool


def test_tenure_check_actually_catches_bad_data(corrupted_customers):
    """Proof that test_tenure_is_non_negative's logic is not a no-op.
    Run the SAME check against corrupted data and confirm it flags the
    injected bad row. If this test ever fails, your validation logic is
    broken -- it's not protecting anything.
    """
    bad_rows = corrupted_customers[corrupted_customers["tenure_months"] < 0]
    assert not bad_rows.empty
    assert bad_rows["customer_id"].tolist() == ["A4"]


# TODO: add a test that monthly_charges is always positive (a $0 or
# negative charge is a data error, not a valid customer).
#
# TODO: add a test using the REAL output of `get_feature_table()` from
# src/data_pipeline.py (once implemented) -- checking there are no
# nulls in any feature column the model will train on. This is the test
# that would have caught a real bug: models silently drop or mis-handle
# NaNs depending on the library, and you won't notice until performance
# tanks in a way that's hard to trace back.
