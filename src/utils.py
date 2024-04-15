import sqlite3
import pandas as pd 
from typing import Optional, Union, Tuple, Dict
import streamlit as st
import os 

def load_data() -> pd.DataFrame:
    """
        These function query the database and return all records as a DataFrame
        returns pd.DataFrame(all_records)...
    """
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(root_dir, "db", "madurai.db")
    with sqlite3.connect(database=db_path) as con :
        statement = "SELECT * FROM donation_records;"
        df = pd.read_sql_query(statement,con, index_col="id")
        return df


def filter_df(df:pd.DataFrame, selected_place:Optional[str]="", selected_book:Optional[str]="") -> pd.DataFrame:

    """
        These function takes used for filtering the data based on two columns
        named(place & book) these two columns actually Optional if we doesn't provide
        any values for that func will return actuall dataframe itself,

        if value for place or book provided, returns the records based on book or place,

        if both are provided apply both conditions and returns the records which satisfy both conditions... 

        returns pd.DataFrame
    
    """

    if selected_book and selected_place: 
        return df[(df["place"] == selected_place) & (df["book"] == selected_book)]
    elif selected_book:
        return df[df["book"] == selected_book]
    elif selected_place:
        return df[df["place"] == selected_place]
    else:
        return df
    


def get_particular_record(id:int) -> Union[pd.DataFrame, bool]:
    """
        This function query the database and return the
        particular record as a DataFrame based on their ID...

        If there is no record found for that ID returns 'False' and
        execute streamlit's error notification.

        for eg, pd.DataFrame({"id":128, "name":"Arjun", "place":"", 
        and some key value pair of ingedients ,"Nei":10, "Sugar":5, "Thu paruppu":0})

    """

    df = load_data().reset_index()
    result = df[df["book_serial_num"] == id]
    if result.empty:
        st.error(f"No records for this ID : {id}, please try with diffrent ID")
        st.stop()
    return result




def get_contribution(particular_record:pd.DataFrame) -> Tuple[Dict[str, str], pd.DataFrame]:

    """
        These function takes particular_record(DataFrame) of a donar as an input
        and returns the tuple of personal_record and ingedient contribution...

        personal_record contains name, place etc and contribution contains
        the details about what are the ingredients they give and how much quantity.

        return tuple(dict, pd.DataFrame)
        for eg, peronsal_record = {"id":128, "name":"Arjun", "place":"", "contact_number":"",
                                    "date":"2024/01/04", "book":"B4"}
                contribution = pd.DataFrame({
                "Product":["Sugar", "Manjal Podi"], "Quantity":[10,5]
                })
    """


    columns = particular_record.to_dict("split")["columns"]
    values  = particular_record.to_dict("split")["data"]
    # we take all non zero records
    non_zero_values = {key:value for key, value in zip(columns, values[0]) if value != 0}
    personal_info_cols = ["id", "name", "place", "contact_number", "date", "book", "book_serial_num"]
    personal_record, contribution, product_list, quantity_list = {}, {}, [], []
    for key, val in non_zero_values.items():
        if key not in personal_info_cols:
            product_list.append(key)
            quantity_list.append(val)
        personal_record[key] = val 
    contribution["Product"] = product_list
    contribution["Quantity"] = quantity_list

    return personal_record, pd.DataFrame(contribution)
    
