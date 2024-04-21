import streamlit as st 
from src.utils import load_data
import sqlite3
import pandas as pd
# from src.utils import get_inventory


def get_units():
    with sqlite3.connect("./db/madurai.db") as con :
        return pd.read_sql("select * from products;", con)

def inventory():
    df = load_data()
    unit_df = get_units()
    
    req_cols = [col for col in df.columns if df[col].dtype != "O"][1:]
    filter_df = df[req_cols].sum().reset_index().rename(columns={'index': 'product', 0 : 'quantity'})

    final_df =  filter_df.merge(unit_df, how='left')
    final_df.index += 1

    return final_df


st.set_page_config(
        page_title="Ingredients Inventory", initial_sidebar_state="collapsed", layout="centered"
)
st.sidebar.image("thirukalyanam.jpg")

st.markdown("**List of products available**")

df = inventory()
st.dataframe(data = df, width=1200, height=500)

col1, col2, col3 = st.columns(3)

if col1.button("Home page", use_container_width=True, key="delete-1", type="primary"):
    st.switch_page("./app.py")
    
elif col2.button("Add page", use_container_width=True, key="delete-2", type="primary"):
    st.switch_page("pages/add.py")
    
elif col3.button("Update page", use_container_width=True, key="delete-3", type="primary"):
    st.switch_page("pages/update.py") 
    

