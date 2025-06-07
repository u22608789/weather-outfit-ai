# extracts features from clothing + preferences
# src/feature_engineering.py

from typing import Dict, List
import math

def extract_features(outfit: Dict, user: Dict, weather: Dict) -> Dict:
    items = outfit["details"]

    total_warmth = sum(i["warmthFactor"] for i in items)
    waterproof_items = [i for i in items if i["waterproof"]]
    waterproof_ratio = len(waterproof_items) / len(items)

    # Style match score
    matching_styles = [i for i in items if i["style"] == user["style"]]
    style_match = len(matching_styles) / len(items)

    # Color match score
    color_match = 0
    for i in items:
        color_match += 1 if is_color_preferred(i["colorHue"], user["preferredColours"]) else 0
    color_match_score = color_match / len(items)

    # Sensitivity match
    # Assume for now: target_warmth = function of temperature
    target_warmth = get_target_warmth(weather["temperature"], user["temperatureSensitivity"])
    warmth_diff = abs(total_warmth - target_warmth)

    return {
        "total_warmth": total_warmth,
        "waterproof_ratio": waterproof_ratio,
        "style_match": style_match,
        "color_match": color_match_score,
        "warmth_diff": warmth_diff
    }

def is_color_preferred(hue: int, preferences: List[Dict]) -> bool:
    for pref in preferences:
        min_hue = pref["min"]
        max_hue = pref["max"]
        if min_hue <= max_hue:
            if min_hue <= hue <= max_hue:
                return True
        else:
            # Handle wrap-around hues (e.g., 355 to 10)
            if hue >= min_hue or hue <= max_hue:
                return True
    return False

def get_target_warmth(temperature: float, sensitivity: int) -> float:
    """
    Adjust target warmth based on user's sensitivity.
    Lower sensitivity (1-3) => needs more warmth
    Higher sensitivity (7-10) => needs less
    """
    base = max(0, 20 - temperature)  # colder → higher base warmth
    adjustment = (5 - sensitivity) * 1.5  # scale -1.5 to +6
    return max(0, base + adjustment)
