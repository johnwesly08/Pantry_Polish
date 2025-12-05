from typing import List, Dict

class RecipeService:
    @staticmethod
    def match_recipes(all_recipes: List[Dict], user_inventory: List[str]) -> List[Dict]:
        """
        The 'Brain'. Compares user inventory against local recipe database.
        Returns recipes sorted by Match Score.
        """
        results = []
        # Convert user inventory to a Set for speed
        pantry_set = set(item.lower() for item in user_inventory)

        for recipe in all_recipes:
            # Parse database string "egg, milk" -> Set {"egg", "milk"}
            r_ingredients = [x.strip().lower() for x in recipe['ingredients'].split(',')]
            r_set = set(r_ingredients)

            # INTERSECTION LOGIC
            owned = pantry_set.intersection(r_set)
            missing = r_set - pantry_set
            
            # Calculate Score
            total_needed = len(r_set)
            score = int((len(owned) / total_needed) * 100)

            # We create a new dict for the UI to use
            results.append({
                **recipe, # Unpack existing data
                "score": score,
                "missing_items": list(missing),
                "owned_count": len(owned)
            })

        # Sort: Highest Match First
        results.sort(key=lambda x: x['score'], reverse=True)
        return results