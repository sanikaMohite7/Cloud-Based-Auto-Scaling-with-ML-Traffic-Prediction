import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle
import os

def train_model():
    # Load traffic data
    data = pd.read_csv("data/traffic.csv")
    
    # Features: hour and minute
    X = data[['hour', 'minute']]
    
    # Target: number of requests
    y = data['requests']
    
    # Initialize and train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Create models directory if it doesn't exist
    os.makedirs("models", exist_ok=True)
    
    # Save the trained model
    pickle.dump(model, open("models/traffic_model.pkl", "wb"))
    
    print("Model trained successfully!")
    print(f"Model saved as: models/traffic_model.pkl")
    
    # Test the model with a sample prediction
    sample_prediction = model.predict([[12, 30]])[0]
    print(f"Sample prediction for 12:30 PM: {int(sample_prediction)} requests")

if __name__ == "__main__":
    train_model()
