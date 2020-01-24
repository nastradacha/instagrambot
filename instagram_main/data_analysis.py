import pandas as pd


df = pd.read_csv('C:/Users/Nastracha/OneDrive/Documents/PriceTargetKPI-Dataset1.csv')
# print(df.head(n=5)) print(df.tail(n=5)) first 5 rows and last 5 rows
# print(df.columns) get column names
# print(df.describe())
# print(df.shape) get size of df
# print(df.dtypes) check data typte
print(df.isnull)