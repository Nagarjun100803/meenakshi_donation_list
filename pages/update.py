import streamlit as st 
import pandas as pd 
from app import load_data
import warnings 
warnings.filterwarnings("ignore")
from src.code import DonationRecord
import time


if "original" not in st.session_state:
    st.session_state["original"] = None
if "edited" not in st.session_state:
    st.session_state["edited"] = None

def produce_non_zero_dict(df:pd.DataFrame)-> dict:
    columns = df.to_dict("split")["columns"]
    values = df.to_dict("split")["data"]
    return {key:val for key, val in zip(columns, values[0]) if val!=0}

def render_df(data:dict)->dict:
    ignore_list = ["id", "name", "place", "contact_number", "date", "book"]
    report = {}
    product_list = []
    quantity_list = []
    for key, value in data.items():
        if key not in ignore_list:
            product_list.append(key)
            quantity_list.append(value)

    report["Product"] = product_list
    report["Quantity"] = quantity_list
    return pd.DataFrame(report)


df = load_data().reset_index()
st.header("Update Details")
st.markdown("<h3 style='text-align:center;'>Try twith either person's ID to update</h3>", unsafe_allow_html=True)
IdCol, NCol = st.columns(2)
search_id = IdCol.number_input("ID", min_value=1, max_value=len(df.index))
res = df[df["id"]==search_id]
dict_ = produce_non_zero_dict(res)
st.session_state["original"] = render_df(dict_)
id, name, contact_number, place, date, book =  dict_["id"], dict_['name'], dict_["contact_number"], dict_["place"], dict_["date"],dict_["book"]
search_name = NCol.text_input("Name", value=name, disabled=True)
with st.form("Update details", clear_on_submit=True):
    st.session_state["edited"] = st.data_editor(st.session_state["original"],
                column_config={
                    "Product" : st.column_config.SelectboxColumn("Product", options=DonationRecord.get_columns()),
                    "Quantity" : st.column_config.NumberColumn("Quant")
                }, num_rows="dynamic", width=690)
    if st.form_submit_button("Update", use_container_width=True):
        if not st.session_state["original"].equals(st.session_state["edited"]):
            data = st.session_state["edited"].to_dict("split")["data"]
            data_dict = {key:value for key,value in data}
            obj = DonationRecord(
                data_dict, name, contact_number,book, place, date, id)
            if obj.update_record(data_dict):
                st.success(f"{obj.name}'s record updated sucessfully")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Something went wrong")
        else:
            st.warning("No Changes Made")


