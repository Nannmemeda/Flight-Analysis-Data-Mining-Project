import streamlit as st
from PIL.Image import Image
from delay import delay_page
from flight_price import price_page
import pandas as pd
import streamlit as st
import joblib as jl
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
import plotly.io as pio
import plotly.graph_objects as go
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from matplotlib import pyplot as plt
from PIL import Image
import base64
import plotly.io as pio

st.set_page_config(page_title='Flight Analysis', page_icon = '✈️')

col1, col2, col3 = st.sidebar.columns([1,8,1])
with col1:
    st.write("")
with col2:
    st.image('cute_flight.png',  use_column_width=True)
with col3:
    st.write("")


app_mode = st.sidebar.selectbox("**Choose a page you want to go**", ["🛩️ Flight Search & Price Prediction", "⏰ Flight Delay Probability Calculator"])

if app_mode == "🛩️ Flight Search & Price Prediction":
    price_page()
else:
    delay_page()


st.sidebar.markdown(" ## About this app 💘")
st.sidebar.markdown("Our app uses advanced machine learning algorithms to provide personalized flight recommendations, taking into account factors such as cost, flexibility, and tolerance for delays. Say goodbye to the overwhelming and time-consuming process of searching for flights, and let our app simplify your travel experience. With our user-friendly interface and personalized recommendations, you can trust that you're getting the best flight options for your unique travel needs. Try it now and make your next trip stress-free.")
st.sidebar.info("Read more about how the model works and see the code on my [Github](https://github.com/Nannmemeda/Flight-Analysis-Data-Mining-Project).", icon="ℹ️")
