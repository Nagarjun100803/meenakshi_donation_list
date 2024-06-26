import streamlit as st 
import pandas as pd 
import time
from src.code import DonationRecord
import sqlite3
from src.utils import load_data, update_iventory_table

def check_new_column(new_col_list : list) -> list:

    new_column = [col for col in new_col_list if col not in DonationRecord.get_columns()]
    
    return new_column



def create_columns(new_col_list : list) -> list:
    with sqlite3.connect("./db/madurai.db") as con:
        cur = con.cursor()
        for col in new_col_list:
            sql = f"""ALTER TABLE donation_records ADD '{col}' INTEGER DEFAULT 0;"""
            cur.execute(sql)
            # sql = f"""ALTER TABLE donation_records_nt ADD '{col}' INTEGER DEFAULT 0;"""
            # cur.execute(sql)
            # sql = f"""INSERT INTO inventory (product, Quantity) values ('{col}', 0);"""
            # cur.execute(sql)
        con.commit()  



def is_exist(book_serial_num : str) -> bool :

    book_serial_nums = load_data()["book_serial_num"].unique()

    return  book_serial_num in book_serial_nums 


st.set_page_config(
    page_title="add-record", initial_sidebar_state="collapsed", layout="centered"
)
st.sidebar.image("thirukalyanam.jpg")
st.markdown("### Add New Contribution")


with st.form("Add details"):

    col1, col2, col3 = st.columns(3)
    name = col2.text_input("Donar Name")
    book = col3.selectbox("Book", ["B"+ str(i) for i in range(20,50)])
    book_serial_num = col1.text_input("Book Serial Number")
    place = col1.text_input("Place", value="Madurai")
    date = col2.date_input("Date")
    contact_number = col3.text_input("Contact Number", max_chars=10)


    ingrident_quantity = st.data_editor(
                    pd.DataFrame(columns=["Product", "Quantity"]),
                    column_config={
                        "Product" : st.column_config.SelectboxColumn(
                            "Product", options=DonationRecord.get_columns(),
                            required=True),


                        "Quantity" : st.column_config.NumberColumn(
                            "Quantity", default=0, 
                            min_value=0)
                    },
                    num_rows="dynamic", 
                    use_container_width=True)
    

    st.markdown("<h6 style='text-align:center;'>Product that we dont have in our database</h6>", unsafe_allow_html=True)

    new_product = st.data_editor(
        pd.DataFrame(columns=["Product", "Quantity"]),
        column_config={
            "Product" : st.column_config.TextColumn(
                "Product", required=True
                ),


            "Quantity" : st.column_config.NumberColumn(
                "Quantity", default=0, 
                min_value=0)
        },
        num_rows="dynamic", 
        use_container_width=True
    )
    # remarks = st.text_input("Remarks")
    button =  st.form_submit_button("Add", use_container_width=True,type="primary")

placeholder = st.empty()

col1, col2, col3 = st.columns(3)

if col1.button("Home page", use_container_width=True, key="add_page_button-1", type="primary"):
    st.switch_page("./app.py")
    
elif col2.button("Update page", use_container_width=True, key="add_page_button-2", type="primary"):
    st.switch_page("pages/update.py")
    
elif col3.button("Delete page", use_container_width=True, key="add_page_button-3", type="primary"):
    st.switch_page("pages/delete.py") 

if button :
    
    if is_exist(book_serial_num):
        placeholder.error("BOOK SERIAL NUMBER ALREADY EXISTS")
        st.stop()

    all_dict = {}

    if (not ingrident_quantity.empty):

        ing_data = ingrident_quantity.to_dict("split")["data"] 
        ing_data_dict = {key:value for key,value in ing_data}
        all_dict.update(ing_data_dict)


    if (not new_product.empty):

        new_data = new_product.to_dict("split")["data"]
        new_data_dict = {key:val for key, val in new_data}
        all_dict.update(new_data_dict)  


    if not(all([name.strip(), place, book_serial_num]) and (not ingrident_quantity.empty or not new_product.empty)):

        placeholder.error("All FIELDS ARE REQUIRED")
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
                update_iventory_table(all_dict,update_type="add")
                placeholder.success(f"{obj.name}'s record inserted sucessfully")
                time.sleep(0.5)
                st.switch_page("./pages/add.py")
                


        except Exception as e:
            st.error((str(e)))     
        


            

