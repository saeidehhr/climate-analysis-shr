import pandas as pd
df = pd.read_csv('data/newData.csv',parse_dates=['dt'])

df = df.dropna(subset=['AverageTemperature'])

new_df = df[df['dt'].dt.year >= 1985]

new_df.to_csv('data/data1985.csv')