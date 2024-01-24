import streamlit as st 
import pandas as pd 
import sqlite3



def load_data() -> pd.DataFrame:
    """
        These function query the database and return all records as a DataFrame
        returns pd.DataFrame(all_records)
    """
    with sqlite3.connect("./data/madurai.db") as con :
        statement = "SELECT * FROM donation_records;"
        df = pd.read_sql_query(statement,con, index_col="id")
        return df


def main():
    st.set_page_config(
        page_title="Meenakshi Thirukalyanam", initial_sidebar_state="collapsed", layout="centered"
    )
    st.markdown("### Meenakshi Thirukalyanam Donars List")
    df = load_data()
    table = st.dataframe(data=df,width=600,use_container_width=True)
    col1, col2, col3 = st.columns(3)
    if col1.button("Add page", use_container_width=True, type="primary"):
        st.switch_page("pages/add.py")
    elif col2.button("Update page", use_container_width=True, type="primary"):
        st.switch_page("pages/update.py")
    elif col3.button("Delete page", use_container_width=True, type="primary"):
        st.switch_page("pages/delete.py")


    


if __name__ == "__main__":
    main()