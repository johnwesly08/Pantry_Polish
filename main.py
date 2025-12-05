import streamlit as st
from src.database import PantryRepository
from src.services import RecipeService
from src.styles import load_css, render_hero, render_card

# --- CONFIG ---
st.set_page_config(page_title="Pantry Polish", page_icon="🥗", layout="wide")
load_css() # Inject the Vibrant UI

# --- INITIALIZATION ---
repo = PantryRepository()
service = RecipeService()

# --- SIDEBAR (INPUT) ---
with st.sidebar:
    st.header("🥕 My Fridge")
    
    with st.form("add_ing", clear_on_submit=True):
        new_item = st.text_input("Add Ingredient", placeholder="e.g. Chicken")
        if st.form_submit_button("Add", use_container_width=True):
            repo.add_item(new_item)
            st.rerun()

    # Inventory Tags
    items = repo.get_inventory()
    if items:
        st.write("---")
        st.caption(f"IN STOCK ({len(items)})")
        
        # Grid for tags
        cols = st.columns(2)
        for i, item in enumerate(items):
            if cols[i % 2].button(f"✕ {item.title()}", key=item):
                repo.remove_item(item)
                st.rerun()
        
        if st.button("Clear All", type="secondary"):
            # Clear logic helper
            for i in items: repo.remove_item(i)
            st.rerun()

# --- MAIN DASHBOARD ---
render_hero()

if not items:
    st.info("👈 Add items to your fridge sidebar to see the magic happen.")
else:
    # 1. Fetch Data
    all_data = repo.get_all_recipes()
    
    # 2. Process Logic
    matches = service.match_recipes(all_data, items)
    
    # 3. Render Grid (3 Columns)
    c1, c2, c3 = st.columns(3)
    columns = [c1, c2, c3]
    
    for idx, recipe in enumerate(matches):
        with columns[idx % 3]:
            render_card(recipe, idx)