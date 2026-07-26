"""
Model definition and wrapper.

Keeping this separate from train.py so the model itself (its hyperparameters,
its architecture) is decoupled from the training loop (data splits, metrics,
serialization). That separation is what lets you swap models later without
rewriting the training script.
"""
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


def build_model(kind: str = "logistic"):
    """Return an unfitted sklearn estimator.

    TODO: implement at least TWO model types and compare them honestly in
    train.py (not just pick whichever gives a better number -- report both,
    and reason about the tradeoff: interpretability vs. raw performance,
    training time, overfitting risk given ~7k rows).

    Start with:
      - "logistic": LogisticRegression(max_iter=1000, class_weight="balanced")
      - "random_forest": RandomForestClassifier(n_estimators=200, class_weight="balanced")

    class_weight="balanced" matters here -- you already confirmed this in
    the REPL: 1,869 of 7,043 customers churned, ~26.5%. If you don't
    account for that, your model will look accurate while being useless:
    a model that predicts "no churn" for every single customer still
    scores ~73.5% accuracy while catching zero actual churners. Look up
    why accuracy is a misleading metric on imbalanced data before you
    trust any number this model gives you -- you'll want precision/recall/
    ROC-AUC instead.
    """
    raise NotImplementedError("TODO: implement build_model")
