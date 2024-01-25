import streamlit as st 
import pandas as pd 
from app import load_data
import warnings 
warnings.filterwarnings("ignore")
from src.code import DonationRecord
import time


if "original_contribution" not in st.session_state:
    st.session_state["original_contribution"] = None
if "edited_contribution" not in st.session_state:
    st.session_state["edited_contribution"] = None


def get_particular_record(id:int) -> pd.DataFrame:
    """
        This function query the database and return the
        particular record as a DataFrame based on their ID... 

        for eg, pd.DataFrame({"id":128, "name":"Arjun", "place":"", 
        and some key value pair of ingedients ,"Nei":10, "Sugar":5, "Thu paruppu":0})
        
    """

    df = load_data().reset_index()
    result = df[df["id"] == id]
    if result.empty:
        st.error(f"No records for this ID : {id}, please try with diffrent ID")
        return False
    return result



def get_contribution(particular_record:pd.DataFrame) -> tuple[dict, pd.DataFrame]:

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
    personal_info_cols = ["id", "name", "place", "contact_number", "date", "book"]
    personal_record = {}
    contribution = {}
    product_list = []
    quantity_list = []
    for key, val in non_zero_values.items():
        if key not in personal_info_cols:
            product_list.append(key)
            quantity_list.append(val)
        personal_record[key] = val 
    contribution["Product"] = product_list
    contribution["Quantity"] = quantity_list

    return personal_record, pd.DataFrame(contribution)
    


st.set_page_config(
    page_title="update-record", initial_sidebar_state="collapsed", layout="centered"
)
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
                    }, num_rows="dynamic", width=690)
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


