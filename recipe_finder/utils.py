#!/usr/bin/env python3

# Utility functions for Recipe Finder
import json
import os
import time
from fractions import Fraction
try:
    from recipe_finder import config
except ModuleNotFoundError:
    import config

# Caching
CACHE_DURATION = 3600  # Cache API calls for 1 hour
api_cache = {}

def format_ingredient_amount(amount):
    """Formats a numeric amount into a more readable string (e.g., fractions)."""
    if amount is None:
        return ""
    if float(amount).is_integer():
        return str(int(amount))
    return str(Fraction(amount).limit_denominator())

def calculate_difficulty(recipe):
    """Calculate the difficulty level for a recipe."""
    cooking_time = recipe.get("readyInMinutes", 0)
    ingredient_count = len(recipe.get("extendedIngredients", []))
    if cooking_time > 60 or ingredient_count > 15:
        return "Hard"
    elif cooking_time > 30 or ingredient_count > 10:
        return "Medium"
    else:
        return "Easy"

def parse_nutritional_info(nutrition):
    """Parse and summarize nutritional information."""
    nutrients = {n["name"]: (n["amount"], n["unit"]) for n in nutrition.get("nutrients", [])}
    calories = nutrients.get("Calories", (0, "kcal"))
    protein = nutrients.get("Protein", (0, "g"))
    sodium = nutrients.get("Sodium", (0, "mg"))
    vitamin_a = nutrients.get("Vitamin A", (0, "% of Daily Needs"))
    
    health_metrics = []
    if protein[0] > 25:
        health_metrics.append("✅ High in Protein")
    if vitamin_a[0] > 20:
        health_metrics.append("✅ Good source of Vitamin A")
    if sodium[0] > 1000:
        health_metrics.append("⚠️ High in Sodium")
    
    score = 50
    if protein[0] > 25: score += 15
    if vitamin_a[0] > 20: score += 15
    if sodium[0] < 500: score += 20
    if calories[0] < 500: score += 10
    
    return {
        "calories": f"{calories[0]} {calories[1]}",
        "health_metrics": health_metrics,
        "nutrition_score": min(score, 100)
    }

# Favorites management
def load_favorites():
    """Loads favorite recipes from a file."""
    if not os.path.exists(config.FAVORITES_FILE):
        return []
    with open(config.FAVORITES_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_favorites(favorites):
    """Saves favorite recipes to a file."""
    with open(config.FAVORITES_FILE, 'w') as f:
        json.dump(favorites, f, indent=4)

# Cache management
def get_from_cache(key):
    """Gets data from cache if it exists and is not expired."""
    if key in api_cache and time.time() - api_cache[key]['timestamp'] < CACHE_DURATION:
        return api_cache[key]['data']
    return None

def set_in_cache(key, data):
    """Sets data in the cache with a timestamp."""
    api_cache[key] = {
        'data': data,
        'timestamp': time.time()
    }
