import pandas as pd
from great_tables import GT, md, html

df = pd.read_csv("/workspaces/The_Bottom_Line/DataExtraction/GOVSSTATETAXTIMESERIES.GS00STATETAX-2026-09-15T175343.csv")
df1 = df.drop(columns = "Coefficient of Variation for Amount (percent) (AMOUNT_CV)")

GT(df1).show()