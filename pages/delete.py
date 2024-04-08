import streamlit as st 
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
from src.code import DonationRecord
from src.utils import get_contribution, get_particular_record
import time


st.set_page_config(
    page_title="delete-record", initial_sidebar_state="collapsed", layout="centered"
)
st.markdown("### Delete Record💢")
st.markdown("##### Find a person with an ID to delete</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
search_id = col1.number_input(label="ID", min_value=1,key="delete-search-id")

particular_record = get_particular_record(search_id)
# if type(particular_record) == pd.DataFrame:
personal_record, contribution = get_contribution(particular_record)
id, name, contact_number, place, date, book, book_serial_num =  personal_record["id"], personal_record['name'], personal_record["contact_number"], personal_record["place"], personal_record["date"],personal_record["book"], personal_record["book_serial_num"]
actual_name = col2.text_input("Name", value=name, disabled=True, key="name-delete")
st.markdown("#### Donar Contribution")
contribution.set_index("Product", inplace=True)
st.dataframe(contribution, use_container_width=True)
if st.button("Delete", use_container_width=True, type="primary"):
    obj = DonationRecord({}, name, contact_number, book, place, date, book_serial_num, id,)
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

    

