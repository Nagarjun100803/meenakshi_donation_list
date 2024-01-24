from src.code import DonationRecord
from app import load_data
import pandas as pd
import streamlit as st 
import warnings
warnings.filterwarnings("ignore")
from pages.update import get_non_zero_columns_asdict, get_contribution_asframe, get_particular_record
import time


st.set_page_config(
    page_title="delete-record", initial_sidebar_state="collapsed", layout="centered"
)
st.markdown("### Delert Record💢")
st.markdown("##### Find a person with an ID to delete</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
search_id = col1.number_input(label="ID", min_value=1,key="delete-search-id")


particular_record = get_particular_record(search_id)
if type(particular_record) == pd.DataFrame:
    non_zero_record = get_non_zero_columns_asdict(particular_record)
    df = get_contribution_asframe(non_zero_record)
    id, name, contact_number, place, date, book =  non_zero_record["id"], non_zero_record['name'], non_zero_record["contact_number"], non_zero_record["place"], non_zero_record["date"],non_zero_record["book"]
    actual_name = col2.text_input("Name", value=name, disabled=True, key="name-delete")
    st.markdown("#### Donar Contribution")
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

    

