import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
                
        div[data-testid="stVerticalBlock"] > div {
            border-radius: 10px;        
        }
                
        div[data-testid="stMetricValue"] {
            font-size: 24px;
            color: #2e7d32;
        }
                
        section[data-testid="stSidebar"] {
            background-color: #f8f9fa;
            border-right: 1px solid #e0e0e0;
        }
                
        div.stButton > button:first-child {
            width: 100%;
            border-radius: 8px;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)
    
def render_recipe_card (meal:dict, score: int, missing: list):
    """Render a visual card for a single recipe."""
    with st.container():
        st.markdown("---")
        col1, col2 = st.columns([1,3])

        with col1:
            st.image(meal['strMealThumb'], use_container_width=True, output_format="JPEG")

        with col2:
            st.subheader(meal['strMeal'])

            if score >= 75: color = "green"
            elif score >= 50: color = "orange"
            else: color = "red"

            st.markdown(f"**Compatibility:** : {color}[**{score}%**]")
            st.progress(score / 100, text=None)

            with st.expander(f"See {len(missing)} Missing Ingredients"):
                st.write(", ".jion(missing))

            if meal.get('strSource'):
                st.markdown(f"[**View Full Instructions **]({meal['strSource']})")