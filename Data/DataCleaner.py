import numpy as np
import pandas as pd

df1 = pd.read_csv('Data/Historical Income Tax Rates and Brackets, 1862-2025.csv', na_values = "NaN", nrows = 7)

print(df1.head())

#