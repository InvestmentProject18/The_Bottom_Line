import numpy
import pandas as pd

df = pd.read_csv('data/Federal_Main_Tax_Table.csv', na_values = "NaN")

print(df.to_string())
print(df.isna().sum())