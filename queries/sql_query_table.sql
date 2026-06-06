USE LeadManagementDB;

CREATE TABLE Product_Category (
    CategoryID INT PRIMARY KEY,
    CategoryName VARCHAR(100),
    Added_By VARCHAR(255),
    Added_Dts TIME
);

CREATE TABLE Product (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(200),
    CategoryID INT,
    Is_Active TINYINT,
    Added_By VARCHAR(255),
    Added_Dts TIME,
    FOREIGN KEY (CategoryID) REFERENCES Product_Category(CategoryID)
);

CREATE TABLE Region (
    RegionID INT PRIMARY KEY,
    RegionName VARCHAR(100),
    Added_By VARCHAR(255),
    Added_Dts TIME
);

CREATE TABLE Territory (
    TerritoryID INT PRIMARY KEY,
    TerritoryName VARCHAR(150),
    RegionID INT,
    Added_By VARCHAR(255),
    Added_Dts TIME,
    FOREIGN KEY (RegionID) REFERENCES Region(RegionID)
);

CREATE TABLE Lead_Status (
    StatusID INT PRIMARY KEY,
    StatusName VARCHAR(100),
    Added_By VARCHAR(255),
    Added_Dts TIME
);

CREATE TABLE Lead_Source (
    LeadSourceID INT PRIMARY KEY,
    LeadSourceName VARCHAR(100),
    Added_By VARCHAR(255),
    Added_Dts TIME
);

CREATE TABLE Lead (
    LeadID INT PRIMARY KEY,
    PersonName VARCHAR(150),
    Gender VARCHAR(20),
    CompanyName VARCHAR(200),
    ContactNo VARCHAR(20),
    Email VARCHAR(255),
    City VARCHAR(100),
    State VARCHAR(100),
    TerritoryID INT,
    RegionID INT,
    ProductID INT,
    StatusID INT,
    LeadSourceID INT,
    BusinessNeed TEXT,
    Lead_Gen_Date DATE,
    Added_By VARCHAR(255),
    Added_Dts TIME,
    ExecutiveID INT,
    FOREIGN KEY (TerritoryID) REFERENCES Territory(TerritoryID),
    FOREIGN KEY (RegionID) REFERENCES Region(RegionID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID),
    FOREIGN KEY (StatusID) REFERENCES Lead_Status(StatusID),
    FOREIGN KEY (LeadSourceID) REFERENCES Lead_Source(LeadSourceID)
);

CREATE TABLE Lead_Follow_Up (
    FollowUpID INT PRIMARY KEY,
    LeadID INT,
    ExecutiveID INT,
    ActionTaken VARCHAR(255),
    Remarks TEXT,
    LeadStatusID INT,
    FollowUpDate DATE,
    Added_By VARCHAR(255),
    Added_Dts TIME,
    Executive_Name VARCHAR(150),
    FOREIGN KEY (LeadID) REFERENCES Lead(LeadID),
    FOREIGN KEY (LeadStatusID) REFERENCES Lead_Status(StatusID)
);