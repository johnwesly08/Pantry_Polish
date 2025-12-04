import streamlit as st
import requests

# --- CONFIGURATION ---
# TheMealDB uses '1' as a free test API key for educational use
BASE_URL = "https://www.themealdb.com/api/json/v1/1/"

st.set_page_config(page_title="Pantry Polish (Free)", page_icon="🥘")

# --- STATE MANAGEMENT ---
if 'pantry' not in st.session_state:
    st.session_state.pantry = []

# --- FUNCTIONS ---
def add_ingredient():
    user_input = st.session_state.new_ingredient.strip().lower()
    if user_input and user_input not in st.session_state.pantry:
        st.session_state.pantry.append(user_input)
    st.session_state.new_ingredient = ""

def remove_ingredient(item):
    st.session_state.pantry.remove(item)

def fetch_recipes_by_ingredient(main_ingredient):
    """
    1. Search for meals containing the main ingredient.
    2. The API only gives IDs/Images here, not full ingredients.
    """
    url = f"{BASE_URL}filter.php?i={main_ingredient}"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get('meals', [])
    except:
        return []

def get_meal_details(meal_id):
    """Fetch full details (ingredients) for a specific meal ID"""
    url = f"{BASE_URL}lookup.php?i={meal_id}"
    response = requests.get(url)
    data = response.json()
    return data['meals'][0] if data['meals'] else None

def calculate_match_score(meal_details, user_pantry):
    """
    Compares recipe ingredients with user pantry.
    Returns: (score, missing_ingredients_list)
    """
    recipe_ingredients = []
    # TheMealDB returns ingredients as strIngredient1, strIngredient2... up to 20
    for i in range(1, 21):
        ing = meal_details.get(f"strIngredient{i}")
        if ing and ing.strip():
            recipe_ingredients.append(ing.lower())

    # Find matches (Simple string matching)
    # Note: This is a basic match (e.g., 'salt' matches 'sea salt')
    matches = 0
    missing = []
    
    for r_ing in recipe_ingredients:
        found = False
        for p_ing in user_pantry:
            if p_ing in r_ing or r_ing in p_ing:
                found = True
                break
        if found:
            matches += 1
        else:
            missing.append(r_ing)
            
    # Calculate percentage
    if not recipe_ingredients: return 0, []
    score = int((matches / len(recipe_ingredients)) * 100)
    return score, missing

# --- UI LAYOUT ---
st.title("🥘 The Pantry Polish (Free Edition)")
st.caption("Cook with what you have. Powered by TheMealDB.")

# 1. INPUT
col1, col2 = st.columns([3, 1])
with col1:
    st.text_input("Add ingredients:", key="new_ingredient", on_change=add_ingredient)

# 2. PANTRY TAGS
if st.session_state.pantry:
    st.write("### Your Pantry:")
    cols = st.columns(len(st.session_state.pantry))
    for i, item in enumerate(st.session_state.pantry):
        if cols[i].button(f"❌ {item}", key=f"btn_{i}"):
            remove_ingredient(item)
            st.rerun()

    # 3. SEARCH LOGIC
    if st.button("Find Recipes", type="primary"):
        # We search using the FIRST ingredient as the "anchor"
        main_ing = st.session_state.pantry[0]
        st.info(f"Searching for recipes based on **{main_ing}** and checking against your other items...")
        
        with st.spinner("Analyzing recipes..."):
            # Step 1: Get candidate meals
            candidates = fetch_recipes_by_ingredient(main_ing)
            
            if candidates:
                scored_results = []
                
                # Step 2: Analyze the top 10 candidates (to keep it fast)
                # We limit to 10 because we have to make an API call for EACH recipe to check ingredients
                for meal in candidates[:10]:
                    details = get_meal_details(meal['idMeal'])
                    score, missing = calculate_match_score(details, st.session_state.pantry)
                    scored_results.append({
                        "details": details,
                        "score": score,
                        "missing": missing
                    })
                
                # Step 3: Sort by highest match score
                scored_results.sort(key=lambda x: x['score'], reverse=True)
                
                # Step 4: Display
                for item in scored_results:
                    meal = item['details']
                    with st.container():
                        st.divider()
                        c1, c2 = st.columns([1, 3])
                        with c1:
                            st.image(meal['strMealThumb'])
                        with c2:
                            st.subheader(meal['strMeal'])
                            st.progress(item['score'] / 100, text=f"Match Score: {item['score']}%")
                            
                            with st.expander("See Missing Ingredients"):
                                st.write(", ".join(item['missing']))
                                st.write(f"[View Instructions]({meal['strSource'] if meal['strSource'] else '#'})")
            else:
                st.warning(f"No recipes found for {main_ing}.")
else:
    st.info("Add ingredients to start! (e.g. Chicken, Rice, Garlic)")