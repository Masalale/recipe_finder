#!/usr/bin/env python3

# API Client for Recipe Finder
import requests
try:
    from recipe_finder import config
except ModuleNotFoundError:
    import config

BASE_URL = "https://api.spoonacular.com"

def search_recipes_by_ingredients(ingredients, number=7):
    """Search for 7 recipes based on a list of ingredients."""
    url = f"{BASE_URL}/recipes/findByIngredients"
    params = {
        "ingredients": ",".join(ingredients),
        "number": number,
        "apiKey": config.API_KEY
    }
    # Check if the ingredients list is empty
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Spoonacular API: {e}")
        return None

def find_recipes_by_cuisine(cuisine, meal_type=None, number=5):
    """Find recipes based on cuisine then meal type."""
    url = f"{BASE_URL}/recipes/complexSearch"
    params = {
        "cuisine": cuisine,
        "number": number,
        "apiKey": config.API_KEY
    }
    if meal_type:
        params["type"] = meal_type
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Spoonacular API: {e}")
        return None

def get_recipe_details(recipe_id):
    """Get details for a specific recipe."""
    url = f"{BASE_URL}/recipes/{recipe_id}/information"
    params = {
        "includeNutrition": True,
        "apiKey": config.API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Spoonacular API: {e}")
        return None
