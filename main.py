import streamlit as st
import pandas as pd
from final_project.scraping_functions import fetch_ebay_data, get_goat_data, extract_shoe_data  # Import the fetch_ebay_data function

def ebay():
    st.title("eBay Shoe Price Tracker")
    
    keyword = st.text_input("Enter the product keyword", "shoes")
    size = st.selectbox("Select Shoe Size", ["1","2","3","4", "5", "6", "7", "8", "9", "10", "11", "12"])
    max_price = st.number_input("Enter the maximum price", min_value=0.0, value=100.0)
    
    if st.button("Fetch Data"):
        items = fetch_ebay_data(keyword, size, max_price)
        if items:
            df = pd.DataFrame(items)
            st.success("Data fetched successfully")
            st.write(df)
            st.line_chart(df[['price']])
        else:
            st.warning("No items found with the given criteria.")

def goat_stockx():
    st.title("Shoe Price Tracker - GOAT/StockX Edition")

    query = st.text_input("Enter the shoe name or keyword", "Air Jordan 1")
    size = st.selectbox("Select Shoe Size", ["1","2","3","4", "5", "6", "7", "8", "9", "10", "11", "12"])
    
    if st.button("Search"):
        st.info("Fetching data from GOAT...")
        results = get_goat_data(query)
        
        if results:
            shoe_data = extract_shoe_data(results, size)
            if shoe_data:
                df = pd.DataFrame(shoe_data)
                st.success("Data fetched successfully")
                st.write(df)
                st.line_chart(df[['price']])
            else:
                st.warning("No shoes found for the selected size.")
        else:
            st.warning("No results found for the given query.")

    st.sidebar.title("About")
    st.sidebar.info(
        """
        This app is designed to track shoe prices from GOAT. Enter the name of the shoe you are looking for and select your size to get the latest prices and availability. 
        The data is scraped in real-time from GOAT.
        """
    )

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["eBay Shoe Price Tracker", "GOAT/StockX Shoe Price Tracker"])
    
    if page == "eBay Shoe Price Tracker":
        ebay()
    elif page == "GOAT/StockX Shoe Price Tracker":
        goat_stockx()

if __name__ == "__main__":
    main()
