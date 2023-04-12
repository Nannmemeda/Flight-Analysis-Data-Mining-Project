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


def price_page():
    # Title
    st.title("🛩️ Flight Search & Price Prediction")

    def load_data():
        # Load data
        df = pd.read_csv('flight data.csv', on_bad_lines='skip')
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
        df['price_by_duration'] = df['price'] / df['duration']

        return df

    df = load_data()

    with st.expander("About this app ℹ️ "):
        st.write("")

        st.markdown(
            """
        Introducing our innovative solution to help travelers find the most suitable flights based on their origin and destination. Our app uses advanced machine learning algorithms to provide personalized flight recommendations, taking into account factors such as cost, flexibility, and tolerance for delays. Say goodbye to the overwhelming and time-consuming process of searching for flights, and let our app simplify your travel experience. With our user-friendly interface and personalized recommendations, you can trust that you're getting the best flight options for your unique travel needs. Try it now and make your next trip stress-free.

        """
        )

        st.write("")

    # KNN = jl.load('KNN.joblib')
    DT = jl.load('DT.joblib')

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
    stop_choice = col2.selectbox("Enter you stops choice  🚏 ", stop_list)
    if stop_choice != "":
        transaction_df = transaction_df[transaction_df['stops'] == stop_choice]

    # Airline name choice
    airline_name_list = [""] + sorted(transaction_df['airline_name'].drop_duplicates().tolist())
    airline_name_choice = st.selectbox("Enter your Airline Company Choice ✈️", airline_name_list)
    if airline_name_choice != "":
        transaction_df = transaction_df[transaction_df['airline_name'] == airline_name_choice]

    # Initializing input values

    input_values = []
    input_columns = ['from_country', 'dest_country', 'airline_name', 'duration', 'stops', 'co2_emissions',
                     'departure_month']

    # From country input
    dict_from_country = {0: 'Algeria', 1: 'Argentina', 2: 'Australia', 3: 'Austria', 4: 'Belgium', 5: 'Brazil',
                         6: 'Canada',
                         7: 'Chile', 8: 'China', 9: 'Columbia', 10: 'Denmark', 11: 'Dublin', 12: 'Egypt',
                         13: 'Ethiopia',
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
    dict_airline_name = {0: 'ANA', 1: 'ASL Airlines', 2: 'Aegean', 3: 'Aer Lingus', 4: 'Aerolineas Argentinas',
                         5: 'Aeromexico', 6: 'Air Algerie', 7: 'Air Arabia', 8: 'Air Arabia Maroc', 9: 'Air Astana',
                         10: 'Air Austral', 11: 'Air Baltic', 12: 'Air Canada', 13: 'Air China', 14: 'Air Dolomiti',
                         15: 'Air Europa', 16: 'Air France', 17: 'Air India', 18: 'Air Macau', 19: 'Air Malta',
                         20: 'Air Mauritius', 21: 'Air Moldova', 22: 'Air New Zealand', 23: 'Air Niugini',
                         24: 'Air Serbia',
                         25: 'Air Seychelles', 26: 'Air Tahiti Nui', 27: 'Air Transat', 28: 'Air-India Express',
                         29: 'AirAsia (India)', 30: 'AirAsia X', 31: 'Aircalin', 32: 'American', 33: 'Arkia',
                         34: 'Asiana',
                         35: 'Austrian', 36: 'Avianca', 37: 'Azores Airlines', 38: 'Azul', 39: 'Bamboo Airways',
                         40: 'Biman', 41: 'Blue Air', 42: 'BoA', 43: 'British Airways', 44: 'Brussels Airlines',
                         45: 'Bulgaria Air', 46: 'COPA', 47: 'CSA', 48: 'Cathay Pacific', 49: 'Cebu Pacific',
                         50: 'China Airlines', 51: 'China Eastern', 52: 'China Southern', 53: 'Corendon', 54: 'Croatia',
                         55: 'Cyprus Airways', 56: 'Delta', 57: 'EVA Air', 58: 'EgyptAir', 59: 'El Al', 60: 'Emirates',
                         61: 'Ethiopian', 62: 'Etihad', 63: 'Eurowings', 64: 'Eurowings Discover', 65: 'Fiji Airways',
                         66: 'Finnair', 67: 'Flair Airlines', 68: 'Fly One', 69: 'Flynas', 70: 'GO FIRST',
                         71: 'Garuda Indonesia', 72: 'Gol', 73: 'Gulf Air', 74: 'Hainan', 75: 'Hawaiian',
                         76: 'Hong Kong Airlines', 77: 'ITA', 78: 'Iberia', 79: 'Iberia Express', 80: 'Icelandair',
                         81: 'IndiGo', 82: 'JAL', 83: 'Jazeera', 84: 'Jet2', 85: 'JetBlue', 86: 'Jetstar',
                         87: 'Juneyao Airlines', 88: 'KLM', 89: 'Kenya Airways', 90: 'Korean Air', 91: 'Kuwait Airways',
                         92: 'LATAM', 93: 'LOT', 94: 'Lanmei Airlines (Cambodia)', 95: 'Loganair', 96: 'Lufthansa',
                         97: 'Luxair', 98: 'MEA', 99: 'MIAT', 100: 'Malaysia Airlines', 101: 'Malindo Air', 102: 'Neos',
                         103: 'Nepal Airlines', 104: 'Nile Air', 105: 'Norwegian', 106: 'Oman Air', 107: 'Pakistan',
                         108: 'Paranair', 109: 'Pegasus', 110: 'Philippine Airlines', 111: 'Qantas',
                         112: 'Qatar Airways',
                         113: 'Rex', 114: 'Royal Air Maroc', 115: 'Royal Brunei', 116: 'Royal Jordanian',
                         117: 'RwandAir',
                         118: 'Ryanair', 119: 'SAS', 120: 'SNCF', 121: 'SWISS', 122: 'Saudia', 123: 'Scoot',
                         124: 'Shandong', 125: 'Shanghai Airlines', 126: 'Shenzhen', 127: 'Sichuan Airlines',
                         128: 'Singapore Airlines', 129: 'Sky Airline', 130: 'Sky Express', 131: 'SpiceJet',
                         132: 'Spirit',
                         133: 'SriLankan', 134: 'SunExpress', 135: 'Swoop', 136: 'TAAG', 137: 'TAROM', 138: 'THAI',
                         139: 'TUI fly', 140: 'Tap Air Portugal', 141: 'Thai Smile', 142: 'Transavia', 143: 'Tunisair',
                         144: 'Turkish Airlines', 145: 'Uni Airways', 146: 'United', 147: 'VOEPASS', 148: 'VietJet Air',
                         149: 'Virgin Atlantic', 150: 'Virgin Australia', 151: 'Vistara', 152: 'Viva Air',
                         153: 'VivaAerobus', 154: 'Volaris', 155: 'Vueling', 156: 'WestJet', 157: 'Wideroe',
                         158: 'Wizz Air', 159: 'XiamenAir', 160: 'easyJet', 161: 'flydubai', 162: 'jetSMART'}
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
        prediction = DT.predict(input_variables)

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

                price_by_airline = flight_final_df.groupby("airline_name")['price_by_duration'].mean().reset_index()
                sorted_price = price_by_airline.sort_values("price_by_duration", ascending=False)

                fig_price = px.bar(sorted_price, x="airline_name", y="price_by_duration", color="airline_name",
                                   labels={"airline_name": "Airline Company",
                                           "price_by_duration": "Price (USD) Per Duration Time"},
                                   title="Airline Companies With The Highest Average Price By Duration Time")

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
