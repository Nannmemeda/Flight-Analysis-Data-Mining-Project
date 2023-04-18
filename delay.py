import pandas as pd
import streamlit as st
import plotly.express as px


def delay_page():
    st.title("⏰ Flight Delay Probability Calculator")

    # Load the dataset
    data = pd.read_csv("Combined_Flights.csv")
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
    # Create a dictionary of state centers
    state_centers = {
        "Alabama": {"lat": 32.806671, "lon": -86.791130},
        "Alaska": {"lat": 61.370716, "lon": -152.404419},
        "Arizona": {"lat": 33.729759, "lon": -111.431221},
        "Arkansas": {"lat": 34.969704, "lon": -92.373123},
        "California": {"lat": 36.116203, "lon": -119.681564},
        "Colorado": {"lat": 39.059811, "lon": -105.311104},
        "Connecticut": {"lat": 41.597782, "lon": -72.755371},
        "Delaware": {"lat": 39.318523, "lon": -75.507141},
        "Florida": {"lat": 27.766279, "lon": -81.686783},
        "Georgia": {"lat": 33.040619, "lon": -83.643074},
        "Hawaii": {"lat": 21.094318, "lon": -157.498337},
        "Idaho": {"lat": 44.240459, "lon": -114.478828},
        "Illinois": {"lat": 40.349457, "lon": -88.986137},
        "Indiana": {"lat": 39.849426, "lon": -86.258278},
        "Iowa": {"lat": 42.011539, "lon": -93.210526},
        "Kansas": {"lat": 38.526600, "lon": -96.726486},
        "Kentucky": {"lat": 37.668140, "lon": -84.670067},
        "Louisiana": {"lat": 31.169546, "lon": -91.867805},
        "Maine": {"lat": 44.693947, "lon": -69.381927},
        "Maryland": {"lat": 39.063946, "lon": -76.802101},
        "Massachusetts": {"lat": 42.230170, "lon": -71.530106},
        "Michigan": {"lat": 43.326618, "lon": -84.536095},
        "Minnesota": {"lat": 45.694454, "lon": -93.900192},
        "Mississippi": {"lat": 32.741646, "lon": -89.678697},
        "Missouri": {"lat": 38.456085, "lon": -92.288368},
        "Montana": {"lat": 46.921925, "lon": -110.454353},
        "Nebraska": {"lat": 41.125370, "lon": -98.268082},
        "Nevada": {"lat": 38.313515, "lon": -117.055374},
        "New Hampshire": {"lat": 43.452492, "lon": -71.563896},
        "New Jersey": {"lat": 40.298904, "lon": -74.521011},
        "New Mexico": {"lat": 34.840515, "lon": -106.248482},
        "New York": {"lat": 42.165726, "lon": -74.948051}, "North Carolina": {"lat": 35.630066, "lon": -79.806419},
        "North Dakota": {"lat": 47.528912, "lon": -99.784012},
        "Ohio": {"lat": 40.388783, "lon": -82.764915},
        "Oklahoma": {"lat": 35.565342, "lon": -96.928917},
        "Oregon": {"lat": 44.572021, "lon": -122.070938},
        "Pennsylvania": {"lat": 40.590752, "lon": -77.209755},
        "Rhode Island": {"lat": 41.680893, "lon": -71.511780},
        "South Carolina": {"lat": 33.856892, "lon": -80.945010},
        "South Dakota": {"lat": 44.299782, "lon": -99.438828},
        "Tennessee": {"lat": 35.747845, "lon": -86.692345},
        "Texas": {"lat": 31.054487, "lon": -97.563461},
        "Utah": {"lat": 40.150032, "lon": -111.862434},
        "Vermont": {"lat": 44.045876, "lon": -72.710686},
        "Virginia": {"lat": 37.769337, "lon": -78.170010},
        "Washington": {"lat": 47.400902, "lon": -121.490494},
        "West Virginia": {"lat": 38.491000, "lon": -80.954570},
        "Wisconsin": {"lat": 44.268543, "lon": -89.616508},
        "Wyoming": {"lat": 42.755966, "lon": -107.302490},
        "District of Columbia": {"lat": 38.895110, "lon": -77.036370},
        "Puerto Rico": {"lat": 18.220833, "lon": -66.590149},
        "Virgin Islands": {"lat": 18.335765, "lon": -64.896335}
    }

    # User inputs
    ListA = [""] + sorted(state_codes.keys())
    selected_state = st.selectbox(":red[Enter your destination state*] 🏞", ListA, key='state_selectbox')
    temp_data = data[data["DestStateName"] == selected_state]

    ListB = [""] + sorted(temp_data['Dest'].unique())
    selected_airport = st.selectbox(":red[Enter your destination airport*] 🛬", ListB, key='airport_selectbox')
    temp_data = temp_data[temp_data["Dest"] == selected_airport]

    ListC = [""] + sorted(temp_data["Airline"].unique())
    selected_airline = st.selectbox(":red[Enter your airline company you will take*] 💼", ListC, key='airline_selectbox')

    import plotly.graph_objects as go

    def create_choropleth(state_data, selected_state):
        fig = px.choropleth(
            state_data,
            locations='state_code',
            locationmode='USA-states',
            color='delay_ratio',
            scope='usa',
            center=state_centers[selected_state],
            color_continuous_scale="Viridis_r",
            labels={'delay_ratio': 'Delay Ratio'},
            title='Flight Delay Ratio by Destination State'
        )
        return fig

    if selected_state != "" and selected_airport != "" and selected_airline != "":
        fig = create_choropleth(state_data, selected_state)
        # Adjust the map dimensions
        fig.update_layout(
            geo=dict(
                scope='usa',
                projection_scale=4,  # Adjust the zoom level here
                center=state_centers[selected_state],
            ),
            autosize=False,
            width=800,
            height=600,
        )

    else:
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
    # Start button
    if st.button("Predict Your Possible Delay Probability 💜") and selected_state != "" and selected_airport != "" and selected_airline != "":
        # Filter the data based on user inputs
        user_filtered_data = data[(data["Airline"] == selected_airline) & (data["Dest"] == selected_airport) & (
                data["DestStateName"] == selected_state)]

        # Calculate the probability of delay
        delayed_user_filtered_data = user_filtered_data[
            (user_filtered_data['DepDelayMinutes'] > 0) | (user_filtered_data['Diverted'] == 1) | (
                    user_filtered_data['Cancelled'] == 1)]
        delay_probability = len(delayed_user_filtered_data) / len(user_filtered_data) if len(
            user_filtered_data) > 0 else 0

        # Display the result with larger font size
        st.write(f"You chose {selected_airline} airline. Your destination is {selected_airport} in {selected_state} state ✨")
        st.markdown(f" ## Your Delay Probability: {delay_probability * 100:.2f}% 🤯")

    # Display the interactive choropleth map
    st.plotly_chart(fig)
