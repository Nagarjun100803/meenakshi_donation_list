import streamlit as st 
import pandas as pd 
import sqlite3



def load_data() -> pd.DataFrame:
    with sqlite3.connect("./data/madurai.db") as con :
        statement = "SELECT * FROM donation_records;"
        df = pd.read_sql_query(statement,con, index_col="id")
        return df


def main():
    df = load_data()
    table = st.dataframe(data=df,width=600,use_container_width=True)

    

    


    


if __name__ == "__main__":
    main()