from datetime import datetime
from pathlib import Path
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from logreg import LogisticRegression

def train_model(data_file, model_file):
    X, y, _ = joblib.load(data_file)
    X = np.array(X)
    y = np.array(y)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LogisticRegression(n_iterations=100000, printnum=400)
    training_log = model.fit(X_train, y_train)
    y_pred = np.array(model.predict(X_test))
    report = classification_report(y_test, y_pred, zero_division=0)
    print("Classification report:")
    print(report)

    joblib.dump(model, model_file)

    print(f"Model saved to {model_file}")
    outputs_dir = Path("outputs")
    outputs_dir.mkdir(parents=True, exist_ok=True)
    log_path = outputs_dir / f"training_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    with log_path.open("w", encoding="utf-8") as log_file:
        if training_log:
            log_file.write(training_log)
        log_file.write("classification_report:\n")
        log_file.write(report)
        log_file.write("\n")
    print(f"Training log saved to {log_path}")

if __name__ == "__main__":
    train_model("data/preprocessed_data.pkl", "models/phishing_detector.pkl")