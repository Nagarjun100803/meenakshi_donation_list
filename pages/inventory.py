import streamlit as st 
from src.utils import load_data
import pandas as pd

def get_inventory():
    df = load_data()
    numeric_columns = df[[col for col in df.columns if df[col].dtype != "O"]].columns[1:].to_list()
    inventory_df = pd.DataFrame(df[numeric_columns].sum())
    inventory_df.columns = ["Quantity"]
    return inventory_df.apply(lambda x: round(x,3))


st.set_page_config(
        page_title="Ingredients Inventory", initial_sidebar_state="collapsed", layout="centered"
    )

st.markdown("**List of products available**")

st.dataframe(data = get_inventory(), width=700, height=500)



