import pandas as pd

df_large = pd.read_csv('Combined_Flights_2022.csv')

sample_size = 3000

df_small = df_large.sample(n = sample_size, random_state = 42)

df_small.to_csv('Combined_Flights.csv')