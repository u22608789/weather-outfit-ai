# runs pipeline: generate → rank → show
# main.py

from src.data_loader import load_users, load_clothing_items
from src.outfit_generator import generate_outfits

if __name__ == '__main__':
    users = load_users()
    items = load_clothing_items()

    # Simulate weather input
    weather = {
        "temperature": 10,
        "condition": "Rain"
    }

    for user in users:
        outfits = generate_outfits(user, items, weather)
        print(f"\nGenerated {len(outfits)} outfits for {user['name']}:\n")
        for outfit in outfits:
            print("Outfit:")
            for item in outfit['details']:
                print(f" - {item['type']} ({item['layer']}, {item['warmthFactor']}/10)")
            print()
