import streamlit as st

ebay_image = "https://static-00.iconduck.com/assets.00/ebay-icon-2048x2048-2vonydav.png"

goat_image = "https://pbs.twimg.com/profile_images/1186271879692091395/j-KkjXxL_400x400.jpg"

stockx_image = "https://i.redd.it/wzwzhkcu4et61.jpg"


st.markdown("""
# **Sneaker Price Tracker**

*The ultimate tool for sneakerheads to stay ahead in the game.*

---""")


col1, col2, col3 = st.columns(3)

with col1:
    st.image(ebay_image, use_column_width=True, caption="eBay")

with col2:
    st.image(goat_image, use_column_width=True, caption="GOAT")

with col3:
    st.image(stockx_image, use_column_width=True, caption="StockX")


st.markdown(""" 

### **Key Features:**

- **Real-Time Data:** Scrapes data from eBay, GOAT, and StockX.
- **Price Comparison:** Seamlessly compare prices, trends, and availability across top marketplaces.
- **Smart Decisions:** Empowering you with insights to find the best deals and track price drops.

*Stay one step ahead with accurate, up-to-date data at your fingertips.*
""")
