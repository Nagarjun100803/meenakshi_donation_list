import streamlit as st
from src.code import DonationRecord, Allocation
import pandas as pd
import time
from src.utils import update_iventory_table, check_all_products_exists




st.set_page_config(
    page_title="allocate-ingredient", initial_sidebar_state="collapsed", layout="centered"
)
st.sidebar.image("thirukalyanam.jpg")
st.markdown("<h3 style = 'text-align:center;'> Allocate a products for a cooking team</h3>", unsafe_allow_html=True)

with st.form("allocation-form"):

    col1, col2, col3 = st.columns(3)

    cooking_team = col1.text_input("Cooking Team Name")
    cooking_supervisor = col2.text_input("Supervisor Name")
    supervisor_mobile = col3.text_input("Supervisor Mobile", max_chars=10)

    dish = col1.text_input("Dish")
    date = col2.date_input("Allocation Date")
    team_members = col3.number_input("Team Member Size", step=1, min_value=1)


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
    
    button = st.form_submit_button("Alloacte Products to Cooking Team", use_container_width=True)
    placeholder = st.empty()
    
    if button :
        if not(all([cooking_supervisor, cooking_team, dish, supervisor_mobile,team_members])):
            placeholder.error("ALL FIELDS ARE REQUIRED")
            st.stop()
        
        ing_data = ingrident_quantity.to_dict("split")["data"] 
        ing_data_dict = {key:value for key,value in ing_data}
        
        try :

            check_all_products_exists(ing_data_dict)

            obj = Allocation(
                team_name = cooking_team, team_supervisor= cooking_supervisor,
                date=date.strftime("%Y-%m-%d"), team_supervisor_contact_number=supervisor_mobile,
                dish=dish, ingredients= ing_data_dict
            )
            
            if obj.insert_record() :
                update_iventory_table(ing_data_dict, update_type="sub")
                placeholder.success(f"Allocated for {cooking_supervisor}")
                time.sleep(1)
                st.switch_page("app.py")

            else :
                placeholder.error("Something went wrong")

        except Exception as e:
            placeholder.error(str(e))