# rule-based outfit builder
# src/outfit_generator.py

from itertools import combinations, product
from typing import List, Dict

# Define required and optional layering categories
REQUIRED_LAYERS = ['base_top', 'footwear']
OPTIONAL_LAYERS = ['mid_top', 'outerwear', 'headwear', 'accessory']

def generate_outfits(user: Dict, clothing_items: List[Dict], weather: Dict) -> List[Dict]:
    user_items = [item for item in clothing_items if item['userId'] == user['id']]
    
    # Separate items by layer
    layer_map = {}
    for item in user_items:
        layer_map.setdefault(item['layer'], []).append(item)

    # Ensure all required layers are available
    for req in REQUIRED_LAYERS:
        if req not in layer_map:
            return []

    outfits = []

    # For each base_top item
    for base in layer_map.get('base_top', []):
        for foot in layer_map.get('footwear', []):
            mids = layer_map.get('mid_top', [])
            outers = layer_map.get('outerwear', [])

            # Optionally combine 0-2 mid layers
            for mid_combo in powerset(mids, max_size=2):
                for outer in outers + [None]:  # allow no outerwear
                    outfit_items = [base, foot] + list(mid_combo)
                    if outer:
                        outfit_items.append(outer)

                    # Apply weather filters
                    if weather.get('condition') == 'Rain' and not any(i['waterproof'] for i in outfit_items):
                        continue
                    
                    outfits.append({
                        "userId": user['id'],
                        "items": [i['id'] for i in outfit_items],
                        "layers": [i['layer'] for i in outfit_items],
                        "details": outfit_items
                    })

    return outfits

def powerset(items: List[Dict], max_size=2):
    result = []
    for r in range(0, max_size+1):
        result.extend(combinations(items, r))
    return result
