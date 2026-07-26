"""
Model performance regression tests -- the core MLOps idea from COMP315.

A model isn't "done" once it trains without crashing. It needs a gate:
if a future change (new feature, different hyperparameter, more data)
makes the model WORSE, CI should fail the same way it would for a broken
unit test. This is what separates "I trained a model once" from
"I run a system that keeps a model honest over time."

This file is intentionally left mostly unimplemented. You need to decide
the threshold yourself, based on what you actually measure in train.py --
don't invent a number, earn it from a real baseline run first.
"""
import pytest
from src.train import train


@pytest.fixture(scope="module")
def trained_metrics():
    return train()


def test_roc_auc_above_baseline(trained_metrics):
    """
    TODO: replace 0.0 with a real threshold.

    Process (do this, don't skip it): run train.py once, look at the
    ROC-AUC it reports, and set the threshold to something slightly BELOW
    that number (e.g. actual - 0.02). That gap is your tolerance for
    natural variance across runs. The point isn't to pass today -- it's
    to catch a regression next month when you're tempted to "simplify"
    the feature pipeline and accidentally break something.
    """
    threshold = 0.0  # TODO: set a real, justified threshold
    assert trained_metrics["roc_auc"] >= threshold, (
        f"ROC-AUC {trained_metrics['roc_auc']:.3f} fell below the "
        f"regression threshold {threshold:.3f}"
    )


# TODO: add a test asserting recall on the churned=True class doesn't
# regress below a threshold either. For churn prediction, missing an
# actual churner (false negative) is usually more costly to a business
# than a false alarm -- your test suite should reflect what actually
# matters, not just overall accuracy.
