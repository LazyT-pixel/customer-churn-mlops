"""
Training script: features -> trained model -> metrics report -> serialized artifact.

Run as: python -m src.train
"""
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
import joblib

from src.data_pipeline import get_feature_table
from src.model import build_model

MODEL_OUT_PATH = "model.joblib"


def train():
    """
    TODO: implement the full loop:
      1. df = get_feature_table()
      2. split into X (features) / y (churned), then train_test_split
         with stratify=y (imbalanced target -- don't skip this)
      3. build_model(...), fit on training set
      4. evaluate on the held-out test set: print classification_report
         AND roc_auc_score (accuracy alone is not enough -- see model.py)
      5. joblib.dump(model, MODEL_OUT_PATH)
      6. return the metrics dict -- test_model_performance.py imports
         this function and asserts on the returned numbers.
    """
    raise NotImplementedError("TODO: implement train()")


if __name__ == "__main__":
    metrics = train()
    print(metrics)
