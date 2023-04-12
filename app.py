import streamlit as st
from delay import delay_page
from flight_price import price_page

st.set_page_config(page_title='Flight Analysis', page_icon = '✈️')
app_mode = st.sidebar.selectbox("Choose a page", ["🛩️ Flight Search & Price Prediction", "Delay Duration"])

if app_mode == "🛩️ Flight Search & Price Prediction":
    price_page()
else:
    delay_page()