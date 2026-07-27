import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)

df = pd.read_excel(
    "odemeler.xlsx",
    sheet_name="FON GELİR-GİDER",
    header=None
)

print(df.head(30))