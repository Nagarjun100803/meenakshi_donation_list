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
st.sidebar.image("thirukalyanam.jpg")


if "original_contribution" not in st.session_state:
    st.session_state["original_contribution"] = None
if "edited_contribution" not in st.session_state:
    st.session_state["edited_contribution"] = None


st.markdown("<h3 style = 'text-align:center;'> Update particular contribution.</h3>", unsafe_allow_html=True)
st.markdown("<h5 style = 'text-align:center;'> Find a contribution by book serial number</h5>", unsafe_allow_html=True)


IdCol, NCol = st.columns(2)
search_id = IdCol.text_input("Serial Number", key="update-search-id")
particular_record = get_particular_record(search_id)



if type(particular_record) == pd.DataFrame:

    personal_record, st.session_state["original_contribution"] = get_contribution(particular_record)
    id, name, contact_number, place, date, book, book_serial_num =  personal_record["id"], personal_record['name'], personal_record["contact_number"], personal_record["place"], personal_record["date"],personal_record["book"], personal_record["book_serial_num"]
    search_name = NCol.text_input("Donar Name", value=name, disabled=True, key="name-update")
    
    
    with st.form("Update details", clear_on_submit=True):

        st.session_state["edited_contribution"] = st.data_editor(
                        st.session_state["original_contribution"],
                        column_config={

                            "Product" : st.column_config.SelectboxColumn(
                                "Product", options=DonationRecord.get_columns(), 
                                required=True),
                            "Quantity" : st.column_config.NumberColumn(
                                "Quantity", required=True)
                        }, 
                        num_rows="dynamic", 
                        use_container_width=True)
        

        if st.form_submit_button("Update", use_container_width=True, type="primary"):

            if not st.session_state["original_contribution"].equals(st.session_state["edited_contribution"]):
                
                existed_product = {key : value for key, value in st.session_state["original_contribution"].to_dict("split")["data"]}
                updated_product = {key : value for key, value in st.session_state["edited_contribution"].to_dict("split")["data"]}
                
                obj = DonationRecord(
                    updated_product, name, contact_number,book, place, date, book_serial_num, id)
                
                if obj.update_record(updated_product):

                    
                    st.success(f"{obj.name}'s record updated sucessfully")
                    time.sleep(1)
                    # st.switch_page("./app.py")
                
                else:
                    st.error("Something went wrong")
            else:
                st.warning("No Changes Made")

col1, col2, col3 = st.columns(3)


if col1.button("Home page", use_container_width=True, key="update_page_button-1", type="primary"):
    st.switch_page("./app.py")
    
elif col2.button("Add page", use_container_width=True, key="update_page_button-2", type="primary"):
    st.switch_page("pages/add.py")
    
elif col3.button("Delete page", use_container_width=True, key="update_page_button-3", type="primary"):
    st.switch_page("pages/delete.py") 
    


