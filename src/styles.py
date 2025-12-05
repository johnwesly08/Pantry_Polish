import streamlit as st

def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700&display=swap');
        .stApp {
            background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
            font-family: 'Outfit', sans-serif;
        }
                
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}

        section[data-testid="stSidebar"] {
            background-color: white;
            box-shadow: 4px 0 15px rgba(0,0,0,0.03);
            border: none;
        }

        .recipe-card {
            background: white;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 10px 25px rgba(0,0,0,0.05);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            margin-bottom: 20px;
            border: 1px solid #f0f0f0;
        }
        .recipe-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        }
                
        h1 { color: #1a1a1a; font-weight: 700; letter-spacing: -1px; }
        p { color: #666; }

        .badge {
            padding: 4px 10px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
        }
        .b-green { background: #dcfce7; color: #166534; }
        .b-orange { background: #ffedd5; color: #9a3412; }
        .b-red { background: #fee2e2; color: #991b1b; }

    </style>
    """, unsafe_allow_html=True)

def render_hero():
    st.markdown("""
        <div style="padding: 20px 0 40px 0;">
            <h1 style="font-size: 3rem; margin:0;">Pantry Polish <span style="color:#6366f1;">.</span></h1>
            <p style="font-size: 1.2rem; color: #64748b;">Turn your leftovers into 5-star meals.</p>
        </div>
    """, unsafe_allow_html=True)

def render_card(recipe, key_idx):
    """Renders the HTML Card for a recipe"""
    score = recipe['score']
    if score == 100: b_class = "b-green"
    elif score >= 50: b_class = "b-orange"
    else: b_class = "b-red"

    missing_text = ", ".join(recipe['missing_items'][:3])
    if len(recipe['missing_items']) > 3: missing_text += "..."
    if not missing_text: missing_text = "Ready to cook!"

    st.markdown(f"""
    <div class="recipe-card">
        <div style="height: 180px; overflow: hidden;">
            <img src="{recipe['image']}" style="width: 100%; height: 100%; object-fit: cover;">
        </div>
        <div style="padding: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <h3 style="margin: 0; font-size: 1.1rem; font-weight: 600;">{recipe['name']}</h3>
                <span class="badge {b_class}">{score}% Match</span>
            </div>
            
            <div style="margin-top: 10px; font-size: 0.9rem; color: #94a3b8; display: flex; gap: 15px;">
                <span>⏱ {recipe['time']}</span>
                <span>🔥 {recipe['cal']} kcal</span>
            </div>
            
            <hr style="border: 0; border-top: 1px solid #f1f5f9; margin: 15px 0;">
            
            <div style="font-size: 0.85rem; color: #64748b;">
                <strong>Missing:</strong> {missing_text}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button(f"Cook this", key=f"btn_{key_idx}", use_container_width=True):
        st.toast(f"Starting cooking mode for {recipe['name']}! 🍳")