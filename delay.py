import pandas as pd
import streamlit as st
import plotly.express as px

# Load the dataset
data = pd.read_csv("Combined_Flights_2022.csv")
state_codes = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
    'District of Columbia': 'DC',
    'Puerto Rico': 'PR',
    'U.S. Virgin Islands': 'VI',
    'Guam': 'GU',
    'American Samoa': 'AS',
    'Northern Mariana Islands': 'MP'
}

# Filter the data for delayed flights
delayed_flights = data[(data['DepDelayMinutes'] > 0) | (data['Diverted'] == 1) | (data['Cancelled'] == 1)]

# Calculate the delay ratio for each destination state
grouped_data = delayed_flights.groupby('DestStateName').size().reset_index(name='delayed_count')
total_flights = data.groupby('DestStateName').size().reset_index(name='total_count')
state_data = pd.merge(grouped_data, total_flights, on='DestStateName')
state_data['delay_ratio'] = state_data['delayed_count'] / state_data['total_count']

# Filter state_data to only include rows where DestStateName is in the state_codes dictionary
state_data = state_data[state_data['DestStateName'].isin(state_codes.keys())]

# Create a new column in the state_data DataFrame containing state abbreviations
state_data['state_code'] = state_data['DestStateName'].apply(lambda x: state_codes[x])

# Create the interactive map chart using Plotly
fig = px.choropleth(
    state_data,
    locations='state_code',
    locationmode='USA-states',
    color='delay_ratio',
    scope='usa',
    color_continuous_scale="Viridis_r",
    labels={'delay_ratio': 'Delay Ratio'},
    title='Flight Delay Ratio by Destination State'
)

# User inputs
st.sidebar.title("Flight Delay Predictor")
selected_airline = st.sidebar.selectbox("Select Airline", data["Airline"].unique())
selected_airport = st.sidebar.selectbox("Select Airport", data["Dest"].unique())
selected_state = st.sidebar.selectbox("Select State", state_codes.keys())

# Filter the data based on user inputs
user_filtered_data = data[(data["Airline"] == selected_airline) & (data["Dest"] == selected_airport) & (data["DestStateName"] == selected_state)]

# Calculate the probability of delay
delayed_user_filtered_data = user_filtered_data[(user_filtered_data['DepDelayMinutes'] > 0) | (user_filtered_data['Diverted'] == 1) | (user_filtered_data['Cancelled'] == 1)]
delay_probability = len(delayed_user_filtered_data) / len(user_filtered_data) if len(user_filtered_data) > 0 else 0

# Display the results
st.title("Flight Delay Predictor")
st.write(f"Airline: {selected_airline}, Airport: {selected_airport}, State: {selected_state}")
st.write(f"Probability of delay: {delay_probability * 100:.2f}%")

# Display the interactive choropleth map
st.plotly_chart(fig)
