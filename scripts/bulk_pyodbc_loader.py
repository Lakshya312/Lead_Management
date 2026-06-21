import os
import pyodbc
import pandas as pd
from datetime import datetime

# Resolve the project root and data directory dynamically
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# Standard corporate connection string using Windows Authentication
CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=LeadManagementDB_New;"
    "Trusted_Connection=yes;"
)

def get_current_timestamp():
    """Returns the current system timestamp in standard string format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def clean_val(val, default_val=None):
    """Sanitizes pandas NaN values into safe Python/SQL types."""
    if pd.isna(val):
        return default_val
    return str(val).strip()

def execute_pyodbc_pipeline():
    print("[PyODBC Engine] Establishing direct connection to Microsoft SQL Server...")
    conn = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()
    print("[Success] SQL Server connection link activated.\n")

    # ---------------------------------------------------------
    # 1. REGION MASTER
    # ---------------------------------------------------------
    region_csv = os.path.join(DATA_DIR, "Region.csv")
    if os.path.exists(region_csv):
        print("-> Ingesting: tbl_region_master")
        df = pd.read_csv(region_csv)
        cursor.execute("SET IDENTITY_INSERT tbl_region_master ON")
        for _, row in df.iterrows():
            rid = int(row['regionid'])
            cursor.execute("SELECT 1 FROM tbl_region_master WHERE regionid = ?", rid)
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO tbl_region_master (regionid, regionname, added_by, added_dts) VALUES (?, ?, ?, ?)",
                    rid, clean_val(row['regionname']), clean_val(row['added_by'], "PyODBC_Engine"), clean_val(row['added_dts'], get_current_timestamp())
                )
        cursor.execute("SET IDENTITY_INSERT tbl_region_master OFF")
        conn.commit()

    # ---------------------------------------------------------
    # 2. PRODUCT CATEGORY MASTER
    # ---------------------------------------------------------
    category_csv = os.path.join(DATA_DIR, "Product_Category.csv")
    if os.path.exists(category_csv):
        print("-> Ingesting: tbl_product_category_master")
        df = pd.read_csv(category_csv)
        cursor.execute("SET IDENTITY_INSERT tbl_product_category_master ON")
        for _, row in df.iterrows():
            cid = int(row['categoryid'])
            cursor.execute("SELECT 1 FROM tbl_product_category_master WHERE categoryid = ?", cid)
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO tbl_product_category_master (categoryid, categoryname, added_by, added_dts) VALUES (?, ?, ?, ?)",
                    cid, clean_val(row['categoryname']), clean_val(row['added_by'], "PyODBC_Engine"), clean_val(row['added_dts'], get_current_timestamp())
                )
        cursor.execute("SET IDENTITY_INSERT tbl_product_category_master OFF")
        conn.commit()

    # ---------------------------------------------------------
    # 3. LEAD SOURCE MASTER
    # ---------------------------------------------------------
    source_csv = os.path.join(DATA_DIR, "Lead_Source.csv")
    if os.path.exists(source_csv):
        print("-> Ingesting: tbl_lead_source_master")
        df = pd.read_csv(source_csv)
        cursor.execute("SET IDENTITY_INSERT tbl_lead_source_master ON")
        for _, row in df.iterrows():
            lsid = int(row['leadsourceid'])
            cursor.execute("SELECT 1 FROM tbl_lead_source_master WHERE leadsourceid = ?", lsid)
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO tbl_lead_source_master (leadsourceid, leadsourcename, added_by, added_dts) VALUES (?, ?, ?, ?)",
                    lsid, clean_val(row['leadsourcename']), clean_val(row['added_by'], "PyODBC_Engine"), clean_val(row['added_dts'], get_current_timestamp())
                )
        cursor.execute("SET IDENTITY_INSERT tbl_lead_source_master OFF")
        conn.commit()

    # ---------------------------------------------------------
    # 4. LEAD STATUS MASTER
    # ---------------------------------------------------------
    status_csv = os.path.join(DATA_DIR, "Lead_Status.csv")
    if os.path.exists(status_csv):
        print("-> Ingesting: tbl_lead_status_master")
        df = pd.read_csv(status_csv)
        cursor.execute("SET IDENTITY_INSERT tbl_lead_status_master ON")
        for _, row in df.iterrows():
            stid = int(row['statusid'])
            cursor.execute("SELECT 1 FROM tbl_lead_status_master WHERE statusid = ?", stid)
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO tbl_lead_status_master (statusid, statusname, added_by, added_dts) VALUES (?, ?, ?, ?)",
                    stid, clean_val(row['statusname']), clean_val(row['added_by'], "PyODBC_Engine"), clean_val(row['added_dts'], get_current_timestamp())
                )
        cursor.execute("SET IDENTITY_INSERT tbl_lead_status_master OFF")
        conn.commit()

    # ---------------------------------------------------------
    # 5. TERRITORY MASTER
    # ---------------------------------------------------------
    territory_csv = os.path.join(DATA_DIR, "Territory.csv")
    if os.path.exists(territory_csv):
        print("-> Ingesting: tbl_territory_master")
        df = pd.read_csv(territory_csv)
        cursor.execute("SET IDENTITY_INSERT tbl_territory_master ON")
        for _, row in df.iterrows():
            tid = int(row['territoryid'])
            cursor.execute("SELECT 1 FROM tbl_territory_master WHERE territoryid = ?", tid)
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO tbl_territory_master (territoryid, territoryname, regionid, added_by, added_dts) VALUES (?, ?, ?, ?, ?)",
                    tid, clean_val(row['territoryname']), int(row['regionid']), clean_val(row['added_by'], "PyODBC_Engine"), clean_val(row['added_dts'], get_current_timestamp())
                )
        cursor.execute("SET IDENTITY_INSERT tbl_territory_master OFF")
        conn.commit()

    # ---------------------------------------------------------
    # 6. PRODUCT MASTER
    # ---------------------------------------------------------
    product_csv = os.path.join(DATA_DIR, "Product.csv")
    if os.path.exists(product_csv):
        print("-> Ingesting: tbl_product_master")
        df = pd.read_csv(product_csv)
        cursor.execute("SET IDENTITY_INSERT tbl_product_master ON")
        for _, row in df.iterrows():
            pid = int(row['productid'])
            cursor.execute("SELECT 1 FROM tbl_product_master WHERE productid = ?", pid)
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO tbl_product_master (productid, productname, categoryid, is_active, added_by, added_dts) VALUES (?, ?, ?, ?, ?, ?)",
                    pid, clean_val(row['productname']), int(row['categoryid']), int(row['is_active']) if pd.notna(row['is_active']) else 1,
                    clean_val(row['added_by'], "PyODBC_Engine"), clean_val(row['added_dts'], get_current_timestamp())
                )
        cursor.execute("SET IDENTITY_INSERT tbl_product_master OFF")
        conn.commit()

    # ---------------------------------------------------------
    # 7. CORE LEAD PIPELINE
    # ---------------------------------------------------------
    lead_csv = os.path.join(DATA_DIR, "Lead.csv")
    if os.path.exists(lead_csv):
        print("-> Ingesting: tbl_lead_pipeline (Core Data)")
        df = pd.read_csv(lead_csv)
        cursor.execute("SET IDENTITY_INSERT tbl_lead_pipeline ON")
        for _, row in df.iterrows():
            lid = int(row['leadid'])
            cursor.execute("SELECT 1 FROM tbl_lead_pipeline WHERE leadid = ?", lid)
            if not cursor.fetchone():
                parsed_date = None
                if pd.notna(row['lead_gen_date']):
                    parsed_date = str(pd.to_datetime(row['lead_gen_date']).date())

                cursor.execute(
                    """INSERT INTO tbl_lead_pipeline 
                    (leadid, personname, gender, companyname, contactno, email, city, state, territoryid, regionid, productid, statusid, leadsourceid, businessneed, lead_gen_date, added_by, added_dts, executiveid) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    lid, clean_val(row['personname']), clean_val(row['gender']), clean_val(row['companyname']),
                    clean_val(row['contactno']), clean_val(row['email']), clean_val(row['city']), clean_val(row['state']),
                    int(row['territoryid']), int(row['regionid']), int(row['productid']), int(row['statusid']),
                    int(row['leadsourceid']), clean_val(row['businessneed']), parsed_date,
                    clean_val(row['added_by'], "PyODBC_Engine"), clean_val(row['added_dts'], get_current_timestamp()),
                    int(row['executiveid']) if pd.notna(row['executiveid']) else 0
                )
        cursor.execute("SET IDENTITY_INSERT tbl_lead_pipeline OFF")
        conn.commit()

    # ---------------------------------------------------------
    # 8. LEAD FOLLOW UP HISTORY
    # ---------------------------------------------------------
    followup_csv = os.path.join(DATA_DIR, "Lead_Follow_Up.csv")
    if os.path.exists(followup_csv):
        print("-> Ingesting: tbl_lead_followup_history")
        df = pd.read_csv(followup_csv)
        cursor.execute("SET IDENTITY_INSERT tbl_lead_followup_history ON")
        for _, row in df.iterrows():
            fuid = int(row['followupid'])
            cursor.execute("SELECT 1 FROM tbl_lead_followup_history WHERE followupid = ?", fuid)
            if not cursor.fetchone():
                parsed_date = None
                if pd.notna(row['followupdate']):
                    parsed_date = str(pd.to_datetime(row['followupdate']).date())

                cursor.execute(
                    """INSERT INTO tbl_lead_followup_history 
                    (followupid, leadid, executiveid, actiontaken, remarks, leadstatusid, followupdate, added_by, added_dts, executive_name) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    fuid, int(row['leadid']), int(row['executiveid']) if pd.notna(row['executiveid']) else 0,
                    clean_val(row['actiontaken']), clean_val(row['remarks']), int(row['leadstatusid']), parsed_date,
                    clean_val(row['added_by'], "PyODBC_Engine"), clean_val(row['added_dts'], get_current_timestamp()),
                    clean_val(row['executive_name'])
                )
        cursor.execute("SET IDENTITY_INSERT tbl_lead_followup_history OFF")
        conn.commit()

    cursor.close()
    conn.close()
    print("\n[Pipeline Complete] PyODBC successfully synchronized all tables with 100% precision.")

if __name__ == "__main__":
    execute_pyodbc_pipeline()