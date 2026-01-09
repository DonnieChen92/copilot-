import joblib
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def train():
    # Load data
    print("Loading data...")
    iris = load_iris()
    X, y = iris.data, iris.target

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    print("Training model...")
    clf = LogisticRegression(max_iter=200)
    clf.fit(X_train, y_train)

    # Evaluate
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {acc:.2f}")

    # Save model
    model_path = 'ml_deployment/model.joblib'
    print(f"Saving model to {model_path}...")
    joblib.dump(clf, model_path)
    print("Done.")

if __name__ == '__main__':
    train()
