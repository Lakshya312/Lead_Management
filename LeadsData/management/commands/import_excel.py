import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings

from LeadsData.models import (
    Product_Category,
    Product,
    Region,
    Territory,
    Lead,
    Lead_Source,
    Lead_Status,
    Lead_Follow_Up
)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        excel_path = os.path.join(
            settings.BASE_DIR,
            "data",
            "Product_Lead_Data_Demo.xlsx"
        )

        if not os.path.exists(excel_path):
            self.stdout.write(self.style.ERROR(f"File not found: {excel_path}"))
            return

        product_df = pd.read_excel(excel_path, sheet_name="Product")
        category_df = pd.read_excel(excel_path, sheet_name="Product_Category")
        region_df = pd.read_excel(excel_path, sheet_name="Region")
        territory_df = pd.read_excel(excel_path, sheet_name="Territory")
        lead_df = pd.read_excel(excel_path, sheet_name="Lead")
        lead_source_df = pd.read_excel(excel_path, sheet_name="Lead_Source")
        lead_status_df = pd.read_excel(excel_path, sheet_name="Lead_Status")
        followup_df = pd.read_excel(excel_path, sheet_name="Lead_Follow_Up")

        # ================= PRODUCT CATEGORY =================
        if "CategoryID" in category_df.columns:
            for _, row in category_df.iterrows():
                Product_Category.objects.get_or_create(
                    CategoryID=row["CategoryID"],
                    defaults={
                        "CategoryName": row.get("CategoryName"),
                        "Added_By": row.get("Added_By", "system"),
                        "Added_Dts": row.get("Added_Dts"),
                    }
                )

        self.stdout.write("Product Category Imported")

        # ================= PRODUCT =================
        if "ProductID" in product_df.columns:
            for _, row in product_df.iterrows():
                Product.objects.get_or_create(
                    ProductID=row["ProductID"],
                    defaults={
                        "ProductName": row["ProductName"],
                        "Category_id": row["CategoryID"],
                        "Is_Active": row.get("Is_Active", True),
                        "Added_By": row.get("Added_By", "system"),
                        "Added_Dts": row.get("Added_Dts"),
                    }
                )

        self.stdout.write("Product Imported")

        # ================= REGION =================
        if "RegionID" in region_df.columns:
            for _, row in region_df.iterrows():
                Region.objects.get_or_create(
                    RegionID=row["RegionID"],
                    defaults={
                        "RegionName": row["RegionName"],
                        "Added_By": row.get("Added_By", "system"),
                        "Added_Dts": row.get("Added_Dts"),
                    }
                )

        self.stdout.write("Region Imported")

        # ================= TERRITORY =================
        if "TerritoryID" in territory_df.columns:
            for _, row in territory_df.iterrows():
                Territory.objects.get_or_create(
                    TerritoryID=row["TerritoryID"],
                    defaults={
                        "TerritoryName": row["TerritoryName"],
                        "Region_id": row.get("RegionID"),
                        "Added_By": row.get("Added_By", "system"),
                        "Added_Dts": row.get("Added_Dts"),
                    }
                )

        self.stdout.write("Territory Imported")

        # ================= LEAD SOURCE =================
        if "LeadSourceID" in lead_source_df.columns:
            for _, row in lead_source_df.iterrows():
                Lead_Source.objects.get_or_create(
                    LeadSourceID=row["LeadSourceID"],
                    defaults={
                        "LeadSourceName": row["LeadSourceName"],
                        "Added_By": row.get("Added_By", "system"),
                        "Added_Dts": row.get("Added_Dts"),
                    }
                )

        self.stdout.write("Lead Source Imported")

        # ================= LEAD STATUS =================
        if "StatusID" in lead_status_df.columns:
            for _, row in lead_status_df.iterrows():
                Lead_Status.objects.get_or_create(
                    StatusID=row["StatusID"],
                    defaults={
                        "StatusName": row["StatusName"],
                        "Added_By": row.get("Added_By", "system"),
                        "Added_Dts": row.get("Added_Dts"),
                    }
                )

        self.stdout.write("Lead Status Imported")

        # ================= LEAD =================
        if "LeadID" in lead_df.columns:
            for _, row in lead_df.iterrows():
                Lead.objects.get_or_create(
                    LeadID=row["LeadID"],
                    defaults={
                        "PersonName": row["PersonName"],
                        "Gender": row.get("Gender"),
                        "CompanyName": row.get("CompanyName"),
                        "ContactNo": row.get("ContactNo"),
                        "Email": row.get("Email"),
                        "City": row.get("City"),
                        "State": row.get("State"),

                        "Territory_id": row.get("TerritoryID"),
                        "Region_id": row.get("RegionID"),
                        "Product_id": row.get("ProductID"),
                        "Status_id": row.get("StatusID"),
                        "Source_id": row.get("LeadSourceID"),

                        "BusinessNeed": row.get("BusinessNeed"),
                        "Lead_Gen_Date": row.get("Lead_Gen_Date"),
                        "Added_By": row.get("Added_By", "system"),
                        "Added_Dts": row.get("Added_Dts"),
                        "ExecutiveID": row.get("ExecutiveID"),
                    }
                )

        self.stdout.write("Lead Imported")

        # ================= LEAD FOLLOW UP =================
        if "FollowUpID" in followup_df.columns:
            for _, row in followup_df.iterrows():
                Lead_Follow_Up.objects.get_or_create(
                    FollowUpID=row["FollowUpID"],
                    defaults={
                        "Lead_id": row["LeadID"],
                        "ExecutiveID": row.get("ExecutiveID"),
                        "ActionTaken": row.get("ActionTaken"),
                        "Remarks": row.get("Remarks"),
                        "LeadStatus_id": row.get("LeadStatusID"),
                        "FollowUpDate": row.get("FollowUpDate"),
                        "Added_By": row.get("Added_By", "system"),
                        "Added_Dts": row.get("Added_Dts"),
                        "Executive_Name": row.get("Executive_Name"),
                    }
                )

        self.stdout.write(self.style.SUCCESS("ALL DATA IMPORTED SUCCESSFULLY 🚀"))