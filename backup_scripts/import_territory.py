import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import pandas as pd
from leadapp.models import Territory, Region

file_path = r"D:\Project\Lead Management\Product_Lead_Data_Demo.xlsx"

df = pd.read_excel(file_path, sheet_name="Territory")

for _, row in df.iterrows():

    region = Region.objects.get(
        RegionID=int(row["RegionID"])
    )

    Territory.objects.create(
        TerritoryID=int(row["TerritoryID"]),
        TerritoryName=str(row["TerritoryName"]),
        RegionID=region,
        Added_By=str(row["Added_By"]),
        Added_Dts=row["Added_Dts"]
    )

print("Territories Imported Successfully")
print("Count =", Territory.objects.count())