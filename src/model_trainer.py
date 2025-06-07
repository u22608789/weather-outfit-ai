# trains and evaluates model
# src/model_trainer.py

import random
import joblib
from typing import List
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error

from src.feature_engineering import extract_features
from src.outfit_generator import generate_outfits

def simulate_user_rating(features):
    """Fake function to simulate a user rating based on extracted features"""
    score = (
        0.3 * features['style_match'] +
        0.3 * features['color_match'] +
        0.2 * (1 - (features['warmth_diff'] / 10)) +  # smaller warmth diff = better
        0.2 * features['waterproof_ratio']
    ) * 5
    return round(min(max(score, 1), 5), 1)  # clamp to 1-5 range

def train_model(users: List[dict], clothing_items: List[dict], weather: dict):
    X, y = [], []

    for user in users:
        outfits = generate_outfits(user, clothing_items, weather)
        for outfit in outfits:
            features = extract_features(outfit, user, weather)
            label = simulate_user_rating(features)

            X.append(list(features.values()))
            y.append(label)

    print(f"Generated training set with {len(X)} examples")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = RandomForestRegressor(n_estimators=100)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    rmse = root_mean_squared_error(y_test, predictions)
    print(f"Model RMSE: {rmse:.2f}")

    joblib.dump(model, 'models/outfit_rating_model.pkl')
    print("Model saved to models/outfit_rating_model.pkl")

    return model
