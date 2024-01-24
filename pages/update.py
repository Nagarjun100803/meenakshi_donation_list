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



def get_non_zero_columns_asdict(df:pd.DataFrame)-> dict:
    """
        This function takes the particular record of person from the
        "get_particular_record()" and will return only the columns 
        which having non zero values as dictionary...
    
        for eg, {"id":128, "name":"Arjun", "place":"", "Nei":10, "Sugar":5} 
    """
    columns = df.to_dict("split")["columns"]
    values = df.to_dict("split")["data"]
    return {key:val for key, val in zip(columns, values[0]) if val!=0}



def get_contribution_asframe(data:dict)->pd.DataFrame:
    """
        This function takes the non zero dictionary as an input from
        "produce_non_zero_dict()" and return only the ingredients/contributions
        provided by the particular record...

        for eg, pd.DataFrame({"Product":["Nei", "Sugar"], "Quantity":[10, 5]})

    """

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



st.set_page_config(
    page_title="update-record", initial_sidebar_state="collapsed", layout="centered"
)
st.markdown("### Update Details 📝")
st.markdown("##### Find a person with an ID to update</h3>", unsafe_allow_html=True)
IdCol, NCol = st.columns(2)
search_id = IdCol.number_input("ID", min_value=1, key="update-search-id")
particular_record = get_particular_record(search_id)


if type(particular_record) == pd.DataFrame:
    non_zero_record = get_non_zero_columns_asdict(particular_record)
    st.session_state["original"] = get_contribution_asframe(non_zero_record)
    id, name, contact_number, place, date, book =  non_zero_record["id"], non_zero_record['name'], non_zero_record["contact_number"], non_zero_record["place"], non_zero_record["date"],non_zero_record["book"]
    search_name = NCol.text_input("Name", value=name, disabled=True, key="name-update")
    with st.form("Update details", clear_on_submit=True):
        st.session_state["edited"] = st.data_editor(st.session_state["original"],
                    column_config={
                        "Product" : st.column_config.SelectboxColumn("Product", options=DonationRecord.get_columns()),
                        "Quantity" : st.column_config.NumberColumn("Quant", default=0, min_value=0)
                    }, num_rows="dynamic", width=690)
        if st.form_submit_button("Update", use_container_width=True, type="primary"):
            if not st.session_state["original"].equals(st.session_state["edited"]):
                data = st.session_state["edited"].to_dict("split")["data"]
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


