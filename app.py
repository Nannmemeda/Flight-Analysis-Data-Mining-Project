
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ CSV ----
@st.cache
# def get_data_from_csv():
df = pd.read_csv("flight data.csv")


# df = get_data_from_csv()

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
from_country = st.sidebar.multiselect(
    "Leaving From:",
    options=df["from_country"].unique(),
    default=df["from_country"].unique()
)

dest_country = st.sidebar.multiselect(
    "Departure From:",
    options=df["dest_country"].unique(),
    default=df["dest_country"].unique(),
)

departure_time = st.sidebar.multiselect(
    "Departure Time:",
    options=df["departure_time"].unique(),
    default=df["departure_time"].unique()
)

arrival_time = st.sidebar.multiselect(
    "Departure Time:",
    options=df["arrival_time"].unique(),
    default=df["arrival_time"].unique()
)


df_selection = df.query(
    "from_country == @from_country & dest_country ==@dest_country & departure_time == @departure_time & arrival_time == @arrival_time"
)

# ---- MAINPAGE ----
st.title(":bar_chart: Flight Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")

# Scatter Chart : duration vs price
fig = px.scatter(df, x='duration', y='price', color='airline_name', size='co2_emissions', hover_data=['from_country', 'dest_country'])

# Show the plot
fig.show()

# top_10 co2_by_airline

# group the data by airline name and sum the CO2 emissions
co2_by_airline = df.groupby("airline_name")["co2_emissions"].sum().reset_index()

# sort the data by CO2 emissions in descending order and select the top 10 airlines
top_10 = co2_by_airline.sort_values("co2_emissions", ascending=False).head(10)

# create the bar chart using Plotly Express
fig = px.bar(top_10, x="airline_name", y="co2_emissions", color="airline_name",
             labels={"airline_name": "Airline Name", "co2_emissions": "Total CO2 Emissions (kg)"},
             title="Top 10 Airlines with the Highest CO2 Emissions")
fig.show()


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
