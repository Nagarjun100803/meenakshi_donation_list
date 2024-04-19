import streamlit as st 
from src.utils import get_inventory


st.set_page_config(
        page_title="Ingredients Inventory", initial_sidebar_state="collapsed", layout="centered"
)
st.sidebar.image("thirukalyanam.jpg")

st.markdown("**List of products available**")

df = get_inventory()
st.dataframe(data = df, width=1200, height=500)

col1, col2, col3 = st.columns(3)

if col1.button("Home page", use_container_width=True, key="delete-1", type="primary"):
    st.switch_page("./app.py")
    
elif col2.button("Add page", use_container_width=True, key="delete-2", type="primary"):
    st.switch_page("pages/add.py")
    
elif col3.button("Update page", use_container_width=True, key="delete-3", type="primary"):
    st.switch_page("pages/update.py") 
    

