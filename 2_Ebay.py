import streamlit as st
import pandas as pd
import numpy as np
from scraping_functions import fetch_ebay_data


#def ebay():
st.title("Shoe Price Tracker - eBay")

keyword = st.text_input("Enter the product keyword", "shoes")
size = str(st.selectbox("Select Shoe Size", np.arange(1,15.5,0.5)))
max_price = st.number_input("Enter the maximum price", min_value=0.0, value=100.0)

if st.button("Fetch Data"):
    with st.spinner('Fetching data from eBay...'):
        items = fetch_ebay_data(keyword, size, max_price)
        if items:
            df = pd.DataFrame(items)
            df.index+=1

            df['Shoe'] = df.apply(lambda row: f'<a href="{row["URL"]}" target="_blank">{row["Shoe"]}</a>', axis=1)
            df['Image'] = df['Image'].apply(lambda x: f'<img src="{x}" width="150">')
            df = df.drop("URL", axis=1)

            st.success("Data fetched successfully")
            st.write(df.to_html(escape=False), unsafe_allow_html=True)

        else:
            st.warning("No items found with the given criteria.")

st.sidebar.title("About")
st.sidebar.info(
        """
        This section is designed to track shoe prices from Ebay. Enter the name of the shoe you are looking for, select your size and put a max price to see latest prices of avalible shoes. 
        The data is scraped in real-time so there may be a slight delays.
        """
    )

