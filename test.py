import pandas as pd

df = pd.read_excel(
    "odemeler.xlsx",
    sheet_name="GİDERLER OCAK 2026",
    header=None
)

for i in range(len(df)):
    if "Kule" in str(df.iloc[i,1]):
        print(df.iloc[i])