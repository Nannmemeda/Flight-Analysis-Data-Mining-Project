import pandas as pd

df_large = pd.read_csv('flight data.csv')

sample_size = 50000

df_small = df_large.sample(n = sample_size, random_state = 42)

df_small.to_csv('flight_data.csv')