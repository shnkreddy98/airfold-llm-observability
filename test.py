import pandas as pd

df = pd.read_parquet("~/Downloads/covid-19_data.parquet")
print(df.head())
print(df.info())

