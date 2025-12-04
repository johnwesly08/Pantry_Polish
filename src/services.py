import requests
import streamlit as st
from typing import List, Dict, Tuple, Set

class RecipeService:
    """
    Handles Business Logic: API communication and Matching Algorithm
    """
    BASE_URL = "https://www.themealdb.com/api/json/v1/1/"

    @staticmethod
    @st.cache_data(ttl=3600)
    def fetch_canditate(main_ingredient: str) -> List[Dict]:
        """Fetches recipe IDs based on the anchor ingredient."""
        url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={main_ingredient}"
        try:
            response = response.get(url, timeout = 5)
            response.raise_for_status()
            data = response.json()
            return  data.get('meals', [])
        except requests.RequestException:
            return []
        
    @staticmethod
    def get_meal_details(meal_id: str) -> Dict:
        """Fetches full metadata for a single recipe."""
        url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
        try:
            response = requests.get(url, timeout = 5)
            data = response.json()
            return data['meals'][0] if data['meals'] else {}
        except requests.RequestException:
            return {}
        
    @staticmethod
    def calculate_match_score(meal_details: Dict, user_pantry: List[str]) -> Tuple[int, List[str]]:
        """
        DASE CORE: Calculates compatibility score using Set Theory.
        """

        recipe_ingredients: Set[str] = set()
        for i in range(1,21):
            ing = meal_details.get(f"strIngredient{i}")
            if ing and ing.strip():
                recipe_ingredients.add(ing.lower().strip())

        if not recipe_ingredients:
            return 0, []
        
        matches = 0
        missing = []
        pantry_set = {p.lower() for p in user_pantry}

        for r_ing in recipe_ingredients:
            if any(p_item in r_ing for p_item in pantry_set):
                matches += 1
            else:
                missing.append(r_ing.title())

        score = int((matches / len(recipe_ingredients)) * 100)
        return score, missing