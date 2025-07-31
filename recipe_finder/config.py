#!/usr/bin/env python3

# Configuration for Recipe Finder
import os
from dotenv import load_dotenv

# Load environment variables
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, '.env')
if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)
else:
    load_dotenv()

# Get API key from env file
API_KEY = os.getenv("SPOONACULAR_API_KEY")
if not API_KEY:
    raise ValueError("Spoonacular API key not found. Please set the SPOONACULAR_API_KEY environment variable.")

#  Config for caching the saved recipies
FAVORITES_FILE = os.path.join(BASE_DIR, "favorites.json")
