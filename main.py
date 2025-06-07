# runs pipeline: generate → rank → show
# main.py

from src.data_loader import load_users, load_clothing_items

if __name__ == '__main__':
    users = load_users()
    items = load_clothing_items()

    print("Users:")
    for user in users:
        print(user)

    print("\nClothing Items:")
    for item in items:
        print(item)
