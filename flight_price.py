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
import random


def price_page():
    # Title
    st.title("🛩️ Flight Search & Price Prediction")
    st.image('flight_bar.png', use_column_width=True)

    def load_data():
        # Load data
        df = pd.read_csv('flight_data.csv', on_bad_lines='skip')
        df = df.drop_duplicates()
        df = df.dropna()

        # Clean the flight_number feature
        df['flight_number'] = df['flight_number'].str.split('|').str[0]

        # Clean the airline_name feature
        df['airline_name'] = df['airline_name'].str.replace('[', '').str.replace(']', '')
        df['airline_name'] = df['airline_name'].str.split('|').str[0]

        df['departure_month'] = pd.to_datetime(df['departure_time']).dt.month
        df['departure_time_exact'] = pd.to_datetime(df['departure_time']).dt.strftime('%m-%d %H:%M')
        df['arrival_time_exact'] = pd.to_datetime(df['arrival_time']).dt.strftime('%m-%d %H:%M')

        # Add the analysis variable
        df['co2'] = df['co2_emissions'] - df['avg_co2_emission_for_this_route']

        return df

    RF = jl.load('RF.joblib')

    # Price Prediction

    df = load_data()
    col1, col2 = st.columns(2)

    # From country choice
    from_country_list = sorted(df['from_country'].drop_duplicates().tolist())
    from_country_choice = col1.selectbox(":red[Enter your departure country*]  🌎 ", from_country_list)
    transaction_df = df[df['from_country'] == from_country_choice]

    # Dest country choice
    dest_country_list = sorted(transaction_df['dest_country'].drop_duplicates().tolist())
    dest_country_choice = col2.selectbox(":red[Enter your destination country*]  🌏 ", dest_country_list)
    transaction_df = transaction_df[transaction_df['dest_country'] == dest_country_choice]

    # Departure month choice
    departure_month_list = [""] + sorted(transaction_df['departure_month'].drop_duplicates().tolist())
    departure_month_choice = col1.selectbox("Enter your departure month \U0001F4C5 ", departure_month_list)
    if departure_month_choice != "":
        transaction_df = transaction_df[transaction_df['departure_month'] == departure_month_choice]

    # Stops choice
    stop_list = [""] + sorted(transaction_df['stops'].drop_duplicates().tolist())
    stop_choice = col2.selectbox("Enter your stops choice  🚏 ", stop_list)
    if stop_choice != "":
        transaction_df = transaction_df[transaction_df['stops'] == stop_choice]

    # Airline name choice
    airline_name_list = [""] + sorted(transaction_df['airline_name'].drop_duplicates().tolist())
    airline_name_choice = st.selectbox("Enter your airline company choice ✈️", airline_name_list)
    if airline_name_choice != "":
        transaction_df = transaction_df[transaction_df['airline_name'] == airline_name_choice]

    # Initializing input values

    input_values = []
    input_columns = ['from_country', 'dest_country', 'airline_name', 'duration', 'stops', 'co2_emissions',
                     'departure_month']

    # From country input
    dict_from_country = {0: 'Algeria', 1: 'Argentina', 2: 'Australia', 3: 'Austria', 4: 'Belgium', 5: 'Brazil', 6: 'Canada',
                         7: 'Chile', 8: 'China', 9: 'Columbia', 10: 'Denmark', 11: 'Dublin', 12: 'Egypt', 13: 'Ethiopia',
                         14: 'France', 15: 'Germany', 16: 'Greece', 17: 'India'}
    for key_from_country, value_from_country in dict_from_country.items():
        if value_from_country == from_country_choice:
            input_values.append(key_from_country)

    # Dest country input
    dict_dest_country = {0: 'Algeria', 1: 'Argentina', 2: 'Australia', 3: 'Austria', 4: 'Belgium', 5: 'Brazil',
                         6: 'Canada',
                         7: 'Chile', 8: 'China', 9: 'Columbia', 10: 'Denmark', 11: 'Dublin', 12: 'Egypt',
                         13: 'Ethiopia',
                         14: 'France', 15: 'Germany', 16: 'Greece', 17: 'India', 18: 'Indonesia', 19: 'Italy',
                         20: 'Japan',
                         21: 'Kenya', 22: 'Malaysia', 23: 'Mexico', 24: 'Morocco', 25: 'Netherlands', 26: 'Norway',
                         27: 'Panama', 28: 'Peru', 29: 'Philippines', 30: 'Portugal', 31: 'Qatar', 32: 'Rome',
                         33: 'Russia',
                         34: 'Singapore', 35: 'South Africa', 36: 'South Korea', 37: 'Spain', 38: 'Sweden',
                         39: 'Taiwan',
                         40: 'Thailand', 41: 'Turkey', 42: 'United Arab Emirates', 43: 'United Kingdom',
                         44: 'United States', 45: 'Vietnam', 46: 'Zurich'}
    for key_dest_country, value_dest_country in dict_dest_country.items():
        if value_dest_country == dest_country_choice:
            input_values.append(key_dest_country)

    # Airline name input
    dict_airline_name = {0: 'ANA', 1: 'ASL Airlines', 2: 'Aegean', 3: 'Aer Lingus',
                         4: 'Aerolineas Argentinas', 5: 'Aeromexico', 6: 'Air Algerie', 7: 'Air Arabia',
                         8: 'Air Arabia Maroc', 9: 'Air Astana', 10: 'Air Baltic', 11: 'Air Canada', 12: 'Air China',
                         13: 'Air Dolomiti', 14: 'Air Europa', 15: 'Air France', 16: 'Air India', 17: 'Air Macau',
                         18: 'Air Malta', 19: 'Air Moldova', 20: 'Air New Zealand', 21: 'Air Serbia', 22: 'Air Tahiti Nui',
                         23: 'Air Transat', 24: 'AirAsia (India)', 25: 'AirAsia X', 26: 'Aircalin', 27: 'American',
                         28: 'Arkia', 29: 'Asiana', 30: 'Austrian', 31: 'Avianca', 32: 'Azores Airlines', 33: 'Azul',
                         34: 'Biman', 35: 'BoA', 36: 'British Airways', 37: 'Brussels Airlines', 38: 'Bulgaria Air', 39: 'COPA',
                         40: 'CSA', 41: 'Cathay Pacific', 42: 'China Airlines', 43: 'China Eastern', 44: 'China Southern',
                         45: 'Croatia', 46: 'Delta', 47: 'EVA Air', 48: 'EgyptAir', 49: 'El Al', 50: 'Emirates', 51: 'Ethiopian',
                         52: 'Etihad', 53: 'Eurowings', 54: 'Eurowings Discover', 55: 'Fiji Airways', 56: 'Finnair', 57: 'Flynas',
                         58: 'GO FIRST', 59: 'Garuda Indonesia', 60: 'Gol', 61: 'Gulf Air', 62: 'Hainan', 63: 'Hawaiian',
                         64: 'Hong Kong Airlines', 65: 'ITA', 66: 'Iberia', 67: 'Icelandair', 68: 'IndiGo', 69: 'JAL',
                         70: 'Jazeera', 71: 'JetBlue', 72: 'Jetstar', 73: 'Juneyao Airlines', 74: 'KLM', 75: 'Kenya Airways',
                         76: 'Korean Air', 77: 'Kuwait Airways', 78: 'LATAM', 79: 'LOT', 80: 'Loganair', 81: 'Lufthansa',
                         82: 'Luxair', 83: 'MEA', 84: 'Malaysia Airlines', 85: 'Neos', 86: 'Nepal Airlines', 87: 'Nile Air',
                         88: 'Norwegian', 89: 'Oman Air', 90: 'Paranair', 91: 'Pegasus', 92: 'Philippine Airlines', 93: 'Qantas',
                         94: 'Qatar Airways', 95: 'Rex', 96: 'Royal Air Maroc', 97: 'Royal Brunei', 98: 'Royal Jordanian',
                         99: 'RwandAir', 100: 'Ryanair', 101: 'SAS', 102: 'SWISS', 103: 'Saudia', 104: 'Scoot', 105: 'Shandong',
                         106: 'Shanghai Airlines', 107: 'Shenzhen', 108: 'Sichuan Airlines', 109: 'Singapore Airlines',
                         110: 'Sky Airline', 111: 'SpiceJet', 112: 'Spirit', 113: 'SriLankan', 114: 'TAROM', 115: 'THAI',
                         116: 'TUI fly', 117: 'Tap Air Portugal', 118: 'Thai Smile', 119: 'Tunisair', 120: 'Turkish Airlines',
                         121: 'United', 122: 'Virgin Atlantic', 123: 'Virgin Australia', 124: 'Vistara', 125: 'Viva Air',
                         126: 'VivaAerobus', 127: 'Volaris', 128: 'Vueling', 129: 'WestJet', 130: 'Wideroe', 131: 'Wizz Air',
                         132: 'XiamenAir', 133: 'easyJet', 134: 'flydubai', 135: 'jetSMART'}
    for key_airline_name, value_airline_name in dict_airline_name.items():
        if airline_name_choice != "":
            if value_airline_name == airline_name_choice:
                input_values.append(key_airline_name)
        else:
            freq_airline_name = transaction_df['airline_name'].value_counts().idxmax()
            if value_airline_name == freq_airline_name:
                input_values.append(key_airline_name)

    # Duration input
    avg_duration = transaction_df['duration'].mean()
    input_values.append(avg_duration)

    # Stop choice input
    if stop_choice != "":
        input_values.append(stop_choice)
    else:
        freq_stops = df['stops'].value_counts().idxmax()
        input_values.append(freq_stops)

    # CO2 Emission input
    avg_co2_emission = transaction_df['co2_emissions'].mean()
    input_values.append(avg_co2_emission)

    # Departure month input
    if departure_month_choice != "":
        input_values.append(departure_month_choice)
    else:
        freq_month = df['departure_month'].value_counts().idxmax()
        input_values.append(freq_month)

    input_variables = pd.DataFrame([input_values], columns=input_columns, dtype=float)

    st.write('\n\n')

    if st.button("Predict Price & Search The Possible Flights 💛"):
        prediction = RF.predict(input_variables)

        # Recommended Flight Lists
        st.write("Here's your recommended flights list: ")
        output_df = pd.DataFrame()

        output_df['Flight Number'] = transaction_df['flight_number']
        output_df['Departure Country'] = transaction_df['from_country']
        output_df['Destination Country'] = transaction_df['dest_country']
        output_df['Airline Company'] = transaction_df['airline_name']
        output_df['Departure Time'] = transaction_df['departure_time_exact']
        output_df['Arrival Time'] = transaction_df['arrival_time_exact']
        output_df['Total Stops'] = transaction_df['stops']
        output_df['Duration (min)'] = transaction_df['duration']
        output_df['CO2 Emission'] = transaction_df['co2_emissions']
        output_df.drop_duplicates(subset=['Flight Number', 'Departure Time', 'Arrival Time'], inplace=True)
        output_df.sort_values(by=['Airline Company', 'Departure Time', 'Total Stops'], inplace=True)
        output_df.reset_index(inplace=True)
        output_df = output_df.drop('index', axis=1)

        st.dataframe(output_df)
        st.write("You have", len(output_df), 'choice(s)!')

        # Price Prediction
        st.markdown(f"**Your predicted cost for the trip: 💰 {float(prediction[0]):.2f}**")

    if st.checkbox("🤔Still struggling with airline selection? Let us help you make the decision!"):
        metric = ['👉 \nCheck the Price💰 Comparison between airline companies!',
                  '👉 \nCheck the CO2 Emission💨 between airline companies!',
                  '👉 \nCheck the stops🚏 - price comparison for the specific airline company!']
        new_slider_01 = [""] + [col for col in metric]
        MetricSlider01 = st.selectbox("Pick the analysis you want us to show 👀", new_slider_01)

        try:
            if MetricSlider01 == '👉 \nCheck the Price💰 Comparison between airline companies!':
                flight_df = df[df['from_country'] == from_country_choice]
                flight_df = flight_df[flight_df['dest_country'] == dest_country_choice]
                if departure_month_choice != "":
                    flight_df = flight_df[flight_df['departure_month'] == departure_month_choice]
                if stop_choice != "":
                    flight_df = flight_df[flight_df['stops'] == stop_choice]

                company_list = sorted(flight_df['airline_name'].drop_duplicates().tolist())
                multiselect = st.multiselect("Select the airline company:", company_list)
                st.write("You selected", len(multiselect), 'airline companies')
                flight_final_df = flight_df[flight_df['airline_name'].isin(multiselect)]

                price_by_airline = flight_final_df.groupby("airline_name")['price'].mean().reset_index()
                sorted_price = price_by_airline.sort_values("price", ascending=False)

                fig_price = px.bar(sorted_price, x="airline_name", y="price", color="airline_name",
                                   labels={"airline_name": "Airline Company",
                                           "price_by_duration": "Average Price (USD)"},
                                   title="Airline Companies With The Highest Average Price")

                st.plotly_chart(fig_price)

            elif MetricSlider01 == '👉 \nCheck the CO2 Emission💨 between airline companies!':
                co2_df = df[df['from_country'] == from_country_choice]
                co2_df = co2_df[co2_df['dest_country'] == dest_country_choice]
                if departure_month_choice != "":
                    co2_df = co2_df[co2_df['departure_month'] == departure_month_choice]
                if stop_choice != "":
                    co2_df = co2_df[co2_df['stops'] == stop_choice]

                company_list = sorted(co2_df['airline_name'].drop_duplicates().tolist())
                multiselect = st.multiselect("Select the airline company:", company_list)
                st.write("You selected", len(multiselect), 'airline companies')
                co2_final_df = co2_df[co2_df['airline_name'].isin(multiselect)]

                co2_by_airline = co2_final_df.groupby("airline_name")['co2'].mean().reset_index()
                sorted_co2 = co2_by_airline.sort_values("co2", ascending=False)

                fig_co2 = px.bar(sorted_co2, x="airline_name", y="co2", color="airline_name",
                                 labels={"airline_name": "Airline Company",
                                         "co2": "Average CO2 Emissions (KG) Above The Standard Emissions"},
                                 title="Airline Companies With The Highest Average CO2 Emissions Above The Standard Emissions")

                st.plotly_chart(fig_co2)

            elif MetricSlider01 == '👉 \nCheck the stops🚏 - price comparison for the specific airline company!':
                stop_df = df[df['from_country'] == from_country_choice]
                stop_df = stop_df[stop_df['dest_country'] == dest_country_choice]

                if airline_name_choice != "":
                    stop_final_df = stop_df[stop_df['airline_name'] == airline_name_choice]
                    fig_stop = px.box(stop_final_df, x="stops", y="price", color="stops",
                                      labels={"stops": "Number of Stops",
                                              "price": "Ticket Price (USD)"},
                                      title=f"Relationship Between Number Of Stops Of {airline_name_choice} Airline Company",
                                      category_orders={"stops": sorted(stop_final_df["stops"].unique())})
                    fig_stop.update_layout(legend={"title": "Number of Stops"})
                    st.plotly_chart(fig_stop)

                else:
                    company_list = [""] + sorted(stop_df['airline_name'].drop_duplicates().tolist())
                    MetricSlider02 = st.selectbox("Select the airline company that you want to check:", company_list)
                    if MetricSlider02 != "":
                        stop_final_df = stop_df[stop_df['airline_name'] == MetricSlider02]
                        fig_stop = px.box(stop_final_df, x="stops", y="price", color="stops",
                                          labels={"stops": "Number of Stops",
                                                  "price": "Ticket Price (USD)"},
                                          title=f"Relationship Between Number Of Stops Of {MetricSlider02} Airline Company",
                                          category_orders={"stops": sorted(stop_final_df["stops"].unique())})
                        fig_stop.update_layout(legend={"title": "Number of Stops"})
                        st.plotly_chart(fig_stop)

        except IndexError:
            st.warning("Throwing an exception!")
