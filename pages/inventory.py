import streamlit as st 
from src.utils import load_data
import pandas as pd
import sqlite3


def get_units():
    with sqlite3.connect("./db/madurai.db") as con :
        df = pd.read_sql("select * from products;", con)
        return df
    


def get_inventory():
    df = load_data()
    numeric_columns = df[[col for col in df.columns if df[col].dtype != "O"]].columns[1:].to_list()

    inventory_df = pd.DataFrame(df[numeric_columns].sum()).reset_index().rename(columns={"index" : "product", 0 : "quantity"})
    inventory_df.apply(lambda x: round(x,3))

    unit_df = get_units()
    final_df =  inventory_df.merge(unit_df, how = "left")
    final_df.index +=1

    return final_df


st.set_page_config(
        page_title="Ingredients Inventory", initial_sidebar_state="collapsed", layout="centered"
)

st.markdown("**List of products available**")

st.dataframe(data = get_inventory(), width=1200, height=500)

col1, col2, col3 = st.columns(3)

if col1.button("Home page", use_container_width=True, key="delete-1", type="primary"):
    st.switch_page("./app.py")
    
elif col2.button("Add page", use_container_width=True, key="delete-2", type="primary"):
    st.switch_page("pages/add.py")
    
elif col3.button("Update page", use_container_width=True, key="delete-3", type="primary"):
    st.switch_page("pages/update.py") 
    

