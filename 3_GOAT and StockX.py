import streamlit as st
import pandas as pd
import numpy as np
import concurrent.futures
import time  # Simulating delay
from scraping_functions import initial_goat_scrape, create_goat_list, get_goat_info
from scraping_functions import initial_stockx_scrape, create_stockx_list, get_stockx_info

st.title("Shoe Price Tracker")

query = st.text_input("Enter the shoe name or keyword", "Air Jordan 1")
size = st.selectbox("Select Shoe Size", np.arange(1,15.5,0.5))

def fetch_goat_data(query, size):
    time.sleep(1)  # Simulate scraping delay
    results_goat = initial_goat_scrape(query)
    if results_goat:
        shoe_data = create_goat_list(results_goat, size)
        if shoe_data:
            df = pd.DataFrame(shoe_data)
            df.index += 1
            df['Shoe'] = df.apply(lambda row: f'<a href="{row["URL"]}" target="_blank">{row["Shoe"]}</a>', axis=1)
            df['Image'] = df['Image'].apply(lambda x: f'<img src="{x}" width="150">')
            df = df.drop("URL", axis=1)
            return df
    return None

def fetch_stockx_data(query, size):
    time.sleep(1)  # Simulate scraping delay
    results_stockx = initial_stockx_scrape(query)
    if results_stockx:
        shoe_data = create_stockx_list(results_stockx, size)
        if shoe_data:
            df = pd.DataFrame(shoe_data)
            df.index += 1
            df['Shoe'] = df.apply(lambda row: f'<a href="{row["URL"]}" target="_blank">{row["Shoe"]}</a>', axis=1)
            df['Image'] = df['Image'].apply(lambda x: f'<img src="{x}" width="150">')
            df = df.drop("URL", axis=1)
            return df
    return None

if st.button("Search"):
    with st.spinner('Fetching data from GOAT and StockX...'):
        # Use ThreadPoolExecutor to run both scraping functions concurrently
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_goat = executor.submit(fetch_goat_data, query, size)
            future_stockx = executor.submit(fetch_stockx_data, query, size)
            
            goat_data = future_goat.result()
            stockx_data = future_stockx.result()

    # Create tabs for GOAT and StockX
    tab1, tab2 = st.tabs(["GOAT", "StockX"])

    with tab1:
        if goat_data is not None:
            st.success("Data fetched successfully from GOAT")
            st.write(goat_data.to_html(escape=False), unsafe_allow_html=True)
        else:
            st.warning("No results found for GOAT.")

    with tab2:
        if stockx_data is not None:
            st.success("Data fetched successfully from StockX")
            st.write(stockx_data.to_html(escape=False), unsafe_allow_html=True)
        else:
            st.warning("No results found for StockX.")

st.sidebar.title("About")
st.sidebar.info(
    """
    This app tracks shoe prices from GOAT and StockX. Enter the name of the shoe you are looking for and select your size to get the latest prices and availability. 
    The data is scraped in real-time so there may be a slight delay.
    """
)
