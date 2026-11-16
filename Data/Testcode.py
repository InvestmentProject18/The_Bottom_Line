import numpy
import pandas as pd

df1 = pd.read_csv('/workspaces/The_Bottom_Line/Data/Historical Income Tax Rates and Brackets, 1862-2025.csv', na_values = "NaN", nrows = 7)

print(df1.to_string())