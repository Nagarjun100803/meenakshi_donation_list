import streamlit as st 
import pandas as pd 
import time
from src.code import DonationRecord
import sqlite3

def check_new_column(list_of_column : list) -> list:
    new_column = [col for col in list_of_column if col not in DonationRecord.get_columns()]
    return new_column

def create_columns(list_of_column : list) -> list:
    with sqlite3.connect("./db/madurai.db") as con:
        cur = con.cursor()
        for col in list_of_column:
            sql = f"""ALTER TABLE donation_records ADD '{col}' INTEGER DEFAULT 0;"""
            cur.execute(sql)
        con.commit()


st.set_page_config(
    page_title="add-record", initial_sidebar_state="collapsed", layout="centered"
)
st.markdown("### Add New Records🖊")

with st.form("Add details"):
    col1, col2, col3 = st.columns(3)
    name = col1.text_input("Name")
    book = col2.selectbox("Book", ["B1", "B2", "B3", "B4", "B5", "B6", "B7"])
    book_serial_num = col3.text_input("Book Serial Number")
    place = col1.text_input("Place")
    date = col2.date_input("Date")
    contact_number = col3.text_input("Contact Number", max_chars=10)
    ingrident_quantity = st.data_editor(pd.DataFrame(columns=["Product", "Quantity"]),
                column_config={
                    "Product" : st.column_config.SelectboxColumn("Product", options=DonationRecord.get_columns(), required=True),
                    "Quantity" : st.column_config.NumberColumn("Quant", default=0, min_value=0)
                    # "Unit" : st.column_config.SelectboxColumn("Unit", default= "Kg",options=["Kg", "L", "Pcs"])
                }, num_rows="dynamic", use_container_width=True)
    st.markdown("<h6 style='text-align:center;'>Product that we dont have in our database</h6>", unsafe_allow_html=True)
    new_product = st.data_editor(
        pd.DataFrame(columns=["Product", "Quantity"]),
        column_config={
            "Product" : st.column_config.TextColumn("Product", required=True, max_chars=30),
            "Quantity" : st.column_config.NumberColumn("Quantity", default=0, min_value=0)
            # "Unit" : st.column_config.SelectboxColumn("Unit",default= "Kg",options=["Kg", "L", "Pcs"])
        },
        num_rows="dynamic", use_container_width=True
    )
    remarks = st.text_input("Remarks")
    if st.form_submit_button("Add", use_container_width=True,type="primary"):
        all_dict = {}
        if (not ingrident_quantity.empty):
            ing_data = ingrident_quantity.to_dict("split")["data"] 
            ing_data_dict = {key:value for key,value in ing_data}
            all_dict.update(ing_data_dict)
        if (not new_product.empty):
            new_data = new_product.to_dict("split")["data"]
            new_data_dict = {key:val for key, val in new_data}
            all_dict.update(new_data_dict)  
        if not(name.strip() != "" and (not ingrident_quantity.empty or not new_product.empty)):
            st.error("Enter all the necessary details to add")
            st.stop()
        else: 
            new_cols = check_new_column(all_dict)
            if len(new_cols) != 0:
                create_columns(new_cols)
            else:
                pass
            obj = DonationRecord(
            all_dict, name, contact_number,book, place, date.strftime("%Y-%m-%d"), book_serial_num)
            try:
                if obj.insert_record():
                    st.success(f"{obj.name}'s record inserted sucessfully")
                    time.sleep(1.5)
                    st.switch_page("./app.py")
            except Exception as e:
                st.error((str(e)))     
            
col1, col2, col3 = st.columns(3)
if col1.button("Home page", use_container_width=True, key="add_page_button-1"):
    st.switch_page("./app.py")
elif col2.button("Update page", use_container_width=True, key="add_page_button-2"):
    st.switch_page("pages/update.py")
elif col3.button("Delete page", use_container_width=True, key="add_page_button-3"):
    st.switch_page("pages/delete.py")         




