-- DROP SCHEMA dbo;

CREATE SCHEMA dbo;
-- LeadManagementDB.dbo.Lead_Source definition

-- Drop table

-- DROP TABLE LeadManagementDB.dbo.Lead_Source;

CREATE TABLE LeadManagementDB.dbo.Lead_Source (
	LeadSourceID int NOT NULL,
	LeadSourceName varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	Added_By varchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	Added_Dts datetime NULL,
	CONSTRAINT PK__Lead_Sou__9FB37DB3EB5EA39B PRIMARY KEY (LeadSourceID)
);


-- LeadManagementDB.dbo.Lead_Status definition

-- Drop table

-- DROP TABLE LeadManagementDB.dbo.Lead_Status;

CREATE TABLE LeadManagementDB.dbo.Lead_Status (
	StatusID int NOT NULL,
	StatusName varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	Added_By varchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	Added_Dts datetime NULL,
	CONSTRAINT PK__Lead_Sta__C8EE20434183AF39 PRIMARY KEY (StatusID)
);


-- LeadManagementDB.dbo.Product_Category definition

-- Drop table

-- DROP TABLE LeadManagementDB.dbo.Product_Category;

CREATE TABLE LeadManagementDB.dbo.Product_Category (
	CategoryID int NOT NULL,
	CategoryName varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	Added_By varchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	Added_Dts datetime NULL,
	CONSTRAINT PK__Product___19093A2B52330909 PRIMARY KEY (CategoryID)
);


-- LeadManagementDB.dbo.Region definition

-- Drop table

-- DROP TABLE LeadManagementDB.dbo.Region;

CREATE TABLE LeadManagementDB.dbo.Region (
	RegionID int NOT NULL,
	RegionName varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	Added_By varchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	Added_Dts datetime NULL,
	CONSTRAINT PK__Region__ACD8444350479C75 PRIMARY KEY (RegionID)
);


-- LeadManagementDB.dbo.auth_group definition

-- Drop table

-- DROP TABLE LeadManagementDB.dbo.auth_group;

CREATE TABLE LeadManagementDB.dbo.auth_group (
	id int IDENTITY(1,1) NOT NULL,
	name nvarchar(150) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	CONSTRAINT PK__auth_gro__3213E83F23953F60 PRIMARY KEY (id),
	CONSTRAINT auth_group_name_a6ea08ec_uniq UNIQUE (name)
);


-- LeadManagementDB.dbo.auth_user definition

-- Drop table

-- DROP TABLE LeadManagementDB.dbo.auth_user;

CREATE TABLE LeadManagementDB.dbo.auth_user (
	id int IDENTITY(1,1) NOT NULL,
	password nvarchar(128) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	last_login datetimeoffset NULL,
	is_superuser bit NOT NULL,
	username nvarchar(150) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	first_name nvarchar(150) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	last_name nvarchar(150) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	email nvarchar(254) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	is_staff bit NOT NULL,
	is_active bit NOT NULL,
	date_joined datetimeoffset NOT NULL,
	CONSTRAINT PK__auth_use__3213E83F79F6063D PRIMARY KEY (id),
	CONSTRAINT auth_user_username_6821ab7c_uniq UNIQUE (username)
);


-- LeadManagementDB.dbo.django_content_type definition

-- Drop table

-- DROP TABLE LeadManagementDB.dbo.django_content_type;

CREATE TABLE LeadManagementDB.dbo.django_content_type (
	id int IDENTITY(1,1) NOT NULL,
	app_label nvarchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	model nvarchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	CONSTRAINT PK__django_c__3213E83FEEEB427D PRIMARY KEY (id)
);
 CREATE UNIQUE NONCLUSTERED INDEX django_content_type_app_label_model_76bd3d3b_uniq ON LeadManagementDB.dbo.django_content_type (  app_label ASC  , model ASC  )  
	 WHERE  ([app_label] IS NOT NULL AND [model] IS NOT NULL)
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;


-- LeadManagementDB.dbo.django_migrations definition

-- Drop table

-- DROP TABLE LeadManagementDB.dbo.django_migrations;

CREATE TABLE LeadManagementDB.dbo.django_migrations (
	id bigint IDENTITY(1,1) NOT NULL,
	app nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	name nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	applied datetimeoffset NOT NULL,
	CONSTRAINT PK__django_m__3213E83F9FA2B46B PRIMARY KEY (id)
);


-- LeadManagementDB.dbo.django_session definition

-- Drop table

-- DROP TABLE LeadManagementDB.dbo.django_session;

CREATE TABLE LeadManagementDB.dbo.django_session (
	session_key nvarchar(40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	session_data nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	expire_date datetimeoffset NOT NULL,
	CONSTRAINT PK__django_s__B3BA0F1F05FDE755 PRIMARY KEY (session_key)
);
 CREATE NONCLUSTERED INDEX django_session_expire_date_a5c62663 ON LeadManagementDB.dbo.django_session (  expire_date ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;


-- LeadManagementDB.dbo.Product definition

-- Drop table

-- DROP TABLE LeadManagementDB.dbo.Product;

CREATE TABLE LeadManagementDB.dbo.Product (
	ProductID int NOT NULL,
	ProductName varchar(200) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	CategoryID int NULL,
	Is_Active tinyint NULL,
	Added_By varchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	Added_Dts datetime NULL,
	CONSTRAINT PK__Product__B40CC6ED80C43C48 PRIMARY KEY (ProductID),
	CONSTRAINT FK__Product__Categor__398D8EEE FOREIGN KEY (CategoryID) REFERENCES LeadManagementDB.dbo.Product_Category(CategoryID)
);


-- LeadManagementDB.dbo.Territory definition

-- Drop table

-- DROP TABLE LeadManagementDB.dbo.Territory;

CREATE TABLE LeadManagementDB.dbo.Territory (
	TerritoryID int NOT NULL,
	TerritoryName varchar(150) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	RegionID int NULL,
	Added_By varchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	Added_Dts datetime NULL,
	CONSTRAINT PK__Territor__2BECD2E4FC3EBB4A PRIMARY KEY (TerritoryID),
	CONSTRAINT FK__Territory__Regio__3E52440B FOREIGN KEY (RegionID) REFERENCES LeadManagementDB.dbo.Region(RegionID)
);


-- LeadManagementDB.dbo.auth_permission definition

-- Drop table

-- DROP TABLE LeadManagementDB.dbo.auth_permission;

CREATE TABLE LeadManagementDB.dbo.auth_permission (
	id int IDENTITY(1,1) NOT NULL,
	name nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	content_type_id int NOT NULL,
	codename nvarchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	CONSTRAINT PK__auth_per__3213E83FD3B8D701 PRIMARY KEY (id),
	CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES LeadManagementDB.dbo.django_content_type(id)
);
 CREATE NONCLUSTERED INDEX auth_permission_content_type_id_2f476e4b ON LeadManagementDB.dbo.auth_permission (  content_type_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
 CREATE UNIQUE NONCLUSTERED INDEX auth_permission_content_type_id_codename_01ab375a_uniq ON LeadManagementDB.dbo.auth_permission (  content_type_id ASC  , codename ASC  )  
	 WHERE  ([content_type_id] IS NOT NULL AND [codename] IS NOT NULL)
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;


-- LeadManagementDB.dbo.auth_user_groups definition

-- Drop table

-- DROP TABLE LeadManagementDB.dbo.auth_user_groups;

CREATE TABLE LeadManagementDB.dbo.auth_user_groups (
	id bigint IDENTITY(1,1) NOT NULL,
	user_id int NOT NULL,
	group_id int NOT NULL,
	CONSTRAINT PK__auth_use__3213E83FA6FA17B0 PRIMARY KEY (id),
	CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES LeadManagementDB.dbo.auth_group(id),
	CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES LeadManagementDB.dbo.auth_user(id)
);
 CREATE NONCLUSTERED INDEX auth_user_groups_group_id_97559544 ON LeadManagementDB.dbo.auth_user_groups (  group_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
 CREATE NONCLUSTERED INDEX auth_user_groups_user_id_6a12ed8b ON LeadManagementDB.dbo.auth_user_groups (  user_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
 CREATE UNIQUE NONCLUSTERED INDEX auth_user_groups_user_id_group_id_94350c0c_uniq ON LeadManagementDB.dbo.auth_user_groups (  user_id ASC  , group_id ASC  )  
	 WHERE  ([user_id] IS NOT NULL AND [group_id] IS NOT NULL)
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;


-- LeadManagementDB.dbo.auth_user_user_permissions definition

-- Drop table

-- DROP TABLE LeadManagementDB.dbo.auth_user_user_permissions;

CREATE TABLE LeadManagementDB.dbo.auth_user_user_permissions (
	id bigint IDENTITY(1,1) NOT NULL,
	user_id int NOT NULL,
	permission_id int NOT NULL,
	CONSTRAINT PK__auth_use__3213E83FC2340682 PRIMARY KEY (id),
	CONSTRAINT auth_user_user_permissions_permission_id_1fbb5f2c_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES LeadManagementDB.dbo.auth_permission(id),
	CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES LeadManagementDB.dbo.auth_user(id)
);
 CREATE NONCLUSTERED INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON LeadManagementDB.dbo.auth_user_user_permissions (  permission_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
 CREATE NONCLUSTERED INDEX auth_user_user_permissions_user_id_a95ead1b ON LeadManagementDB.dbo.auth_user_user_permissions (  user_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
 CREATE UNIQUE NONCLUSTERED INDEX auth_user_user_permissions_user_id_permission_id_14a6b632_uniq ON LeadManagementDB.dbo.auth_user_user_permissions (  user_id ASC  , permission_id ASC  )  
	 WHERE  ([user_id] IS NOT NULL AND [permission_id] IS NOT NULL)
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;


-- LeadManagementDB.dbo.django_admin_log definition

-- Drop table

-- DROP TABLE LeadManagementDB.dbo.django_admin_log;

CREATE TABLE LeadManagementDB.dbo.django_admin_log (
	id int IDENTITY(1,1) NOT NULL,
	action_time datetimeoffset NOT NULL,
	object_id nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	object_repr nvarchar(200) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	action_flag smallint NOT NULL,
	change_message nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	content_type_id int NULL,
	user_id int NOT NULL,
	CONSTRAINT PK__django_a__3213E83FB242E79D PRIMARY KEY (id),
	CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES LeadManagementDB.dbo.django_content_type(id),
	CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES LeadManagementDB.dbo.auth_user(id)
);
 CREATE NONCLUSTERED INDEX django_admin_log_content_type_id_c4bce8eb ON LeadManagementDB.dbo.django_admin_log (  content_type_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
 CREATE NONCLUSTERED INDEX django_admin_log_user_id_c564eba6 ON LeadManagementDB.dbo.django_admin_log (  user_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
ALTER TABLE LeadManagementDB.dbo.django_admin_log WITH NOCHECK ADD CONSTRAINT django_admin_log_action_flag_a8637d59_check CHECK (([action_flag]>=(0)));


-- LeadManagementDB.dbo.Lead definition

-- Drop table

-- DROP TABLE LeadManagementDB.dbo.Lead;

CREATE TABLE LeadManagementDB.dbo.Lead (
	LeadID int NOT NULL,
	PersonName varchar(150) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	Gender varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	CompanyName varchar(200) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	ContactNo varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	Email varchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	City varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	State varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	TerritoryID int NULL,
	RegionID int NULL,
	ProductID int NULL,
	StatusID int NULL,
	LeadSourceID int NULL,
	BusinessNeed text COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	Lead_Gen_Date date NULL,
	Added_By varchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	Added_Dts datetime NULL,
	ExecutiveID int NULL,
	CONSTRAINT PK__Lead__73EF791A06334534 PRIMARY KEY (LeadID),
	CONSTRAINT FK__Lead__LeadSource__48CFD27E FOREIGN KEY (LeadSourceID) REFERENCES LeadManagementDB.dbo.Lead_Source(LeadSourceID),
	CONSTRAINT FK__Lead__ProductID__46E78A0C FOREIGN KEY (ProductID) REFERENCES LeadManagementDB.dbo.Product(ProductID),
	CONSTRAINT FK__Lead__RegionID__45F365D3 FOREIGN KEY (RegionID) REFERENCES LeadManagementDB.dbo.Region(RegionID),
	CONSTRAINT FK__Lead__StatusID__47DBAE45 FOREIGN KEY (StatusID) REFERENCES LeadManagementDB.dbo.Lead_Status(StatusID),
	CONSTRAINT FK__Lead__TerritoryI__44FF419A FOREIGN KEY (TerritoryID) REFERENCES LeadManagementDB.dbo.Territory(TerritoryID)
);


-- LeadManagementDB.dbo.Lead_Follow_Up definition

-- Drop table

-- DROP TABLE LeadManagementDB.dbo.Lead_Follow_Up;

CREATE TABLE LeadManagementDB.dbo.Lead_Follow_Up (
	FollowUpID int NOT NULL,
	LeadID int NULL,
	ExecutiveID int NULL,
	ActionTaken varchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	Remarks text COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	LeadStatusID int NULL,
	FollowUpDate date NULL,
	Added_By varchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	Added_Dts datetime NULL,
	Executive_Name varchar(150) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	CONSTRAINT PK__Lead_Fol__D507D658846F06B1 PRIMARY KEY (FollowUpID),
	CONSTRAINT FK__Lead_Foll__LeadI__4BAC3F29 FOREIGN KEY (LeadID) REFERENCES LeadManagementDB.dbo.Lead(LeadID),
	CONSTRAINT FK__Lead_Foll__LeadS__4CA06362 FOREIGN KEY (LeadStatusID) REFERENCES LeadManagementDB.dbo.Lead_Status(StatusID)
);


-- LeadManagementDB.dbo.auth_group_permissions definition

-- Drop table

-- DROP TABLE LeadManagementDB.dbo.auth_group_permissions;

CREATE TABLE LeadManagementDB.dbo.auth_group_permissions (
	id bigint IDENTITY(1,1) NOT NULL,
	group_id int NOT NULL,
	permission_id int NOT NULL,
	CONSTRAINT PK__auth_gro__3213E83FCB32E803 PRIMARY KEY (id),
	CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES LeadManagementDB.dbo.auth_group(id),
	CONSTRAINT auth_group_permissions_permission_id_84c5c92e_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES LeadManagementDB.dbo.auth_permission(id)
);
 CREATE NONCLUSTERED INDEX auth_group_permissions_group_id_b120cbf9 ON LeadManagementDB.dbo.auth_group_permissions (  group_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
 CREATE UNIQUE NONCLUSTERED INDEX auth_group_permissions_group_id_permission_id_0cd325b0_uniq ON LeadManagementDB.dbo.auth_group_permissions (  group_id ASC  , permission_id ASC  )  
	 WHERE  ([group_id] IS NOT NULL AND [permission_id] IS NOT NULL)
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
 CREATE NONCLUSTERED INDEX auth_group_permissions_permission_id_84c5c92e ON LeadManagementDB.dbo.auth_group_permissions (  permission_id ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;