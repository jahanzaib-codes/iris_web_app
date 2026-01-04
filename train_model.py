from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import joblib  # Better than pickle for sklearn models
import os

def train_and_save_model():
    """Train the Iris classification model and save it."""
    
    # Step 1: Load the Iris dataset
    print("📊 Loading Iris dataset...")
    iris = load_iris()
    X = iris.data  # Features: sepal length, sepal width, petal length, petal width
    y = iris.target  # Labels: 0=Setosa, 1=Versicolor, 2=Virginica
    
    # Step 2: Split into training and testing sets
    print("🔀 Splitting data into train/test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Step 3: Train the KNN model
    print("🧠 Training KNN classifier...")
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(X_train, y_train)
    
    # Step 4: Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"✅ Model Accuracy: {accuracy * 100:.2f}%")
    
    # Step 5: Save the model using joblib
    model_path = os.path.join(os.path.dirname(__file__), 'model.joblib')
    joblib.dump(model, model_path)
    print(f"💾 Model saved to: {model_path}")
    
    # Also save the target names for prediction display
    target_names = iris.target_names.tolist()
    target_path = os.path.join(os.path.dirname(__file__), 'target_names.joblib')
    joblib.dump(target_names, target_path)
    print(f"📝 Target names saved to: {target_path}")
    
    return model, accuracy

if __name__ == "__main__":
    print("=" * 50)
    print("🌸 IRIS MODEL TRAINING")
    print("=" * 50)
    train_and_save_model()
    print("=" * 50)
    print("✨ Training complete! You can now run app.py")
    print("=" * 50)
