import streamlit as st 
from src.utils import load_data, filter_df



def main():
    st.set_page_config(
        page_title="Meenakshi Thirukalyanam", initial_sidebar_state="auto", layout="centered"
    )
    st.markdown("### Meenakshi Thirukalyanam Donars List")
    col1, col2 = st.columns(2)
    df = load_data().replace(to_replace={0 : ""})
    places = df["place"].unique().tolist()
    place_option = [""] + places 
    selected_place = col1.selectbox("Place", place_option)
    books = df["book"].unique().tolist()
    book_options = [""] + books
    selected_book = col2.selectbox("Book", book_options)
    result = filter_df(df, selected_place, selected_book)
    if result.empty:
        st.error("No records found")
    else:
        st.dataframe(result, use_container_width=True)

    # columns for buttons
    col3, col4, col5 = st.columns(3)
    if col3.button("Add page", use_container_width=True, type="primary"):
        st.switch_page("pages/add.py")
    elif col4.button("Update page", use_container_width=True, type="primary"):
        st.switch_page("pages/update.py")
    elif col5.button("Delete page", use_container_width=True, type="primary"):
        st.switch_page("pages/delete.py")


    


if __name__ == "__main__":
    main()