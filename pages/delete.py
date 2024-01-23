from src.code import DonationRecord
from app import load_data
import pandas as pd
import streamlit as st 
import warnings
warnings.filterwarnings("ignore")
from pages.update import produce_non_zero_dict, render_df, get_particular_record
import time

df = load_data().reset_index()
col1, col2 = st.columns(2)
search_id = col1.number_input(label="ID", min_value=1,key="delete-search-id")


particular_record = get_particular_record(search_id)
if type(particular_record) == pd.DataFrame:
    dict_ = produce_non_zero_dict(particular_record)
    df = render_df(dict_)
    id, name, contact_number, place, date, book =  dict_["id"], dict_['name'], dict_["contact_number"], dict_["place"], dict_["date"],dict_["book"]
    actual_name = col2.text_input("Name", value=name, disabled=True, key="name-delete")
    st.markdown("###                      Details about the donar")
    st.dataframe(df, use_container_width=True)
    if st.button("Delete", use_container_width=True, type="primary"):
        obj = DonationRecord({}, name, contact_number, book, place, date, id)
        if obj.delete_record():
            st.success(f"{name}'s record is deleted successfully..")
            time.sleep(1)
            st.switch_page("./app.py")
        else:
            st.error("Something went wrong..")

col1, col2, col3 = st.columns(3)
if col1.button("Home page", use_container_width=True, key="delete-1"):
    st.switch_page("./app.py")
elif col2.button("Add page", use_container_width=True, key="delete-2"):
    st.switch_page("pages/add.py")
elif col3.button("Update page", use_container_width=True, key="delete-3"):
    st.switch_page("pages/update.py") 

    

