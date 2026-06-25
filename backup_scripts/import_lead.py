import os
import django
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from leadapp.models import (
    Lead,
    Product,
    Region,
    Territory,
    LeadStatus,
    LeadSource
)

file_path = r"D:\Project\Lead Management\Product_Lead_Data_Demo.xlsx"

df = pd.read_excel(
    file_path,
    sheet_name="Lead"
)

for _, row in df.iterrows():

    Lead.objects.create(

        LeadID=int(row["LeadID"]),

        PersonName=str(row["PersonName"]),

        Gender=str(row["Gender"]),

        CompanyName=str(row["CompanyName"]),

        ContactNo=str(row["ContactNo"]),

        Email=str(row["Email"]),

        City=str(row["City"]),

        State=str(row["State"]),
        ExecutiveID=int(row["ExecutiveID"]),

        TerritoryID=Territory.objects.get(
            TerritoryID=int(row["TerritoryID"])
        ),

        RegionID=Region.objects.get(
            RegionID=int(row["RegionID"])
        ),

        ProductID=Product.objects.get(
            ProductID=int(row["ProductID"])
        ),

        StatusID=LeadStatus.objects.get(
            StatusID=int(row["StatusID"])
        ),

        LeadSourceID=LeadSource.objects.get(
            LeadSourceID=int(row["LeadSourceID"])
        ),

        BusinessNeed=str(row["BusinessNeed"]),

        Lead_Gen_Date=row["Lead_Gen_Date"],

        Added_By=str(row["Added_By"]),

        Added_Dts=row["Added_Dts"]
    )

print("Leads Imported Successfully")
print("Count =", Lead.objects.count())