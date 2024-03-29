import streamlit as st 
import pandas as pd 
import time
from src.code import DonationRecord


st.set_page_config(
    page_title="add-record", initial_sidebar_state="collapsed", layout="centered"
)
st.markdown("### Add New Records🖊")

with st.form("Add details"):
    col1, col2 = st.columns([2,1])
    with col1:
        name = st.text_input("Name")
    with col2:
        place = st.text_input("Place")
    col3, col4, col5 = st.columns(3)
    date = col3.date_input("Date")
    book = col4.selectbox("Book", ["B1", "B2", "B3", "B4", "B5", "B6", "B7"])
    contact_number = col5.text_input("Contact Number")
    ingrident_quantity = st.data_editor(pd.DataFrame(columns=["Product", "Quantity"]),
                column_config={
                    "Product" : st.column_config.SelectboxColumn("Product", options=DonationRecord.get_columns()),
                    "Quantity" : st.column_config.NumberColumn("Quant", default=0, min_value=0)
                }, num_rows="dynamic", use_container_width=True)
    if st.form_submit_button("Add", use_container_width=True,type="primary"):
        if (not ingrident_quantity.empty) and (not name.strip() == ""):
            data = ingrident_quantity.to_dict("split")["data"] 
            data_dict = {key:value for key,value in data}
            obj = DonationRecord(
            data_dict, name, contact_number,book, place, date.strftime("%Y-%m-%d"))
            if obj.insert_record():
                st.success(f"{obj.name}'s record inserted sucessfully")
                time.sleep(1.5)
                st.switch_page("./app.py")
            else:
                st.warning("Something went wrong. Please check you entered all the necesaary details")
        else:
            st.error("Enter necessary details to insert/add...")
        
col1, col2, col3 = st.columns(3)
if col1.button("Home page", use_container_width=True, key="add_page_button-1"):
    st.switch_page("./app.py")
elif col2.button("Update page", use_container_width=True, key="add_page_button-2"):
    st.switch_page("pages/update.py")
elif col3.button("Delete page", use_container_width=True, key="add_page_button-3"):
    st.switch_page("pages/delete.py")         





