# runs pipeline: generate → rank → show
# main.py

from src.data_loader import load_users, load_clothing_items
from src.outfit_generator import generate_outfits
from src.feature_engineering import extract_features
from src.model_trainer import train_model

if __name__ == '__main__':
    users = load_users()
    items = load_clothing_items()

    # Simulated weather
    weather = {
        "temperature": 10,
        "condition": "Rain"
    }

    # Train the model
    model = train_model(users, items, weather)

    # Test: generate outfits and extract features
    for user in users:
        outfits = generate_outfits(user, items, weather)
        print(f"\nGenerated {len(outfits)} outfits for {user['name']}:\n")

        for outfit in outfits:
            print("Outfit:")
            for item in outfit['details']:
                print(f" - {item['type']} ({item['layer']}, {item['warmthFactor']}/10)")
            features = extract_features(outfit, user, weather)
            print("Features:", features)
            print()
