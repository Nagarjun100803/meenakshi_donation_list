import streamlit as st 
import pandas as pd 
import warnings 
warnings.filterwarnings("ignore")
from src.code import DonationRecord
from src.utils import get_particular_record, get_contribution
import time


st.set_page_config(
    page_title="update-record", initial_sidebar_state="collapsed", layout="centered"
)
if "original_contribution" not in st.session_state:
    st.session_state["original_contribution"] = None
if "edited_contribution" not in st.session_state:
    st.session_state["edited_contribution"] = None


st.markdown("### Update Details 📝")
st.markdown("##### Find a person with an ID to update</h3>", unsafe_allow_html=True)
IdCol, NCol = st.columns(2)
search_id = IdCol.number_input("ID", min_value=1, key="update-search-id")
particular_record = get_particular_record(search_id)


if type(particular_record) == pd.DataFrame:
    personal_record, st.session_state["original_contribution"] = get_contribution(particular_record)
    id, name, contact_number, place, date, book =  personal_record["id"], personal_record['name'], personal_record["contact_number"], personal_record["place"], personal_record["date"],personal_record["book"]
    search_name = NCol.text_input("Name", value=name, disabled=True, key="name-update")
    with st.form("Update details", clear_on_submit=True):
        st.session_state["edited_contribution"] = st.data_editor(st.session_state["original_contribution"],
                    column_config={
                        "Product" : st.column_config.SelectboxColumn("Product", options=DonationRecord.get_columns()),
                        "Quantity" : st.column_config.NumberColumn("Quant", default=0, min_value=0)
                    }, num_rows="dynamic", use_container_width=True)
        if st.form_submit_button("Update", use_container_width=True, type="primary"):
            if not st.session_state["original_contribution"].equals(st.session_state["edited_contribution"]):
                data = st.session_state["edited_contribution"].to_dict("split")["data"]
                data_dict = {key:value for key,value in data}
                obj = DonationRecord(
                    data_dict, name, contact_number,book, place, date, id)
                if obj.update_record(data_dict):
                    st.success(f"{obj.name}'s record updated sucessfully")
                    time.sleep(1.5)
                    st.switch_page("./app.py")
                else:
                    st.error("Something went wrong")
            else:
                st.warning("No Changes Made")

col1, col2, col3 = st.columns(3)
if col1.button("Home page", use_container_width=True, key="update_page_button-1"):
    st.switch_page("./app.py")
elif col2.button("Add page", use_container_width=True, key="update_page_button-2"):
    st.switch_page("pages/add.py")
elif col3.button("Delete page", use_container_width=True, key="update_page_button-3"):
    st.switch_page("pages/delete.py") 


