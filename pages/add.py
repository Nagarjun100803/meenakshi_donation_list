import streamlit as st 
import pandas as pd 
import time
from src.code import DonationRecord


st.header("Add New Records")
dummy_df = {
"Product" : [None],
"Quantity" : [None]
}

with st.form("Add details", clear_on_submit=True):
    col1, col2 = st.columns([2,1])
    with col1:
        name = st.text_input("Name")
    with col2:
        place = st.text_input("Place")
    col3, col4, col5 = st.columns(3)
    date = col3.date_input("Date")
    book = col4.selectbox("Book", ["B1", "B2", "B3", "B4", "B5", "B6", "B7"])
    contact_number = col5.text_input("Contact Number")
    ingrident_quantity = st.data_editor(pd.DataFrame(dummy_df),
                column_config={
                    "Product" : st.column_config.SelectboxColumn("Product", options=DonationRecord.get_columns()),
                    "Quantity" : st.column_config.NumberColumn("Quant")
                }, num_rows="dynamic", width=690)
    if st.form_submit_button("Add", use_container_width=True):
        data = ingrident_quantity.to_dict("split")["data"]
        data_dict = {key:value for key,value in data}
        if (tuple(data_dict.keys())[0]) is not None or (name != ""):
            obj = DonationRecord(
            data_dict, name, contact_number,book, place, date.strftime("%Y-%m-%d"))
            if obj.insert_record():
                st.success(f"{obj.name}'s record inserted sucessfully")
                time.sleep(1)
                st.rerun()
            else:
                st.warning("Something went wrong")
        else:
            st.error("Enter necessary details to insert/add...")
        
                 





