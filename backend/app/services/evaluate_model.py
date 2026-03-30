import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score


def run_evaluation():
    print("🚀 Running AML Model Evaluation...")

    # Load data
    features = pd.read_csv("data/elliptic/elliptic_txs_features.csv", header=None)
    classes = pd.read_csv("data/elliptic/elliptic_txs_classes.csv")

    # Rename columns
    features.rename(columns={0: "tx_id"}, inplace=True)
    classes.columns = ["tx_id", "label"]

    # Merge datasets
    df = features.merge(classes, on="tx_id")

    # Remove unknown labels
    df = df[df["label"] != "unknown"]

    # Fix label encoding
    df["label"] = df["label"].replace({
        "1": 1, "2": 0,
        1: 1, 2: 0,
        "illicit": 1, "licit": 0
    })

    # Drop any remaining NaN labels
    df = df.dropna(subset=["label"])

    # Features and target
    X = df.drop(columns=["tx_id", "label"])
    y = df["label"]

    # Train-test split
    X_train, X_test, y_train, y_test, tx_train, tx_test = train_test_split(
        X, y, df["tx_id"], test_size=0.2, random_state=42
    )

    # Model
    model = LogisticRegression(max_iter=500, n_jobs=-1)
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Metrics
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)

    print("\n📊 Classification Report:")
    print(classification_report(y_test, y_pred))
    print(f"\n✅ Accuracy: {acc:.4f}")

    # Save metrics (for dashboard)
    metrics = {
        "accuracy": acc,
        "precision_illicit": report["1"]["precision"],
        "recall_illicit": report["1"]["recall"],
        "f1_illicit": report["1"]["f1-score"]
    }

    with open("backend/app/model_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print("\n💾 Metrics saved → backend/app/model_metrics.json")

    # Save predictions for Neo4j
    results = pd.DataFrame({
        "tx_id": tx_test,
        "actual": y_test,
        "predicted": y_pred
    })

    results.to_csv("backend/app/predictions.csv", index=False)

    print("💾 Predictions saved → backend/app/predictions.csv")

    return model


if __name__ == "__main__":
    run_evaluation()
