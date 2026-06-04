# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Lead(models.Model):
    leadid = models.IntegerField(db_column='LeadID', primary_key=True)  # Field name made lowercase.
    personname = models.CharField(db_column='PersonName', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    companyname = models.CharField(db_column='CompanyName', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    contactno = models.CharField(db_column='ContactNo', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    territoryid = models.ForeignKey('Territory', models.DO_NOTHING, db_column='TerritoryID', blank=True, null=True)  # Field name made lowercase.
    regionid = models.ForeignKey('Region', models.DO_NOTHING, db_column='RegionID', blank=True, null=True)  # Field name made lowercase.
    productid = models.ForeignKey('Product', models.DO_NOTHING, db_column='ProductID', blank=True, null=True)  # Field name made lowercase.
    statusid = models.ForeignKey('LeadStatus', models.DO_NOTHING, db_column='StatusID', blank=True, null=True)  # Field name made lowercase.
    leadsourceid = models.ForeignKey('LeadSource', models.DO_NOTHING, db_column='LeadSourceID', blank=True, null=True)  # Field name made lowercase.
    businessneed = models.TextField(db_column='BusinessNeed', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    lead_gen_date = models.DateField(db_column='Lead_Gen_Date', blank=True, null=True)  # Field name made lowercase.
    added_by = models.CharField(db_column='Added_By', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_dts = models.DateTimeField(db_column='Added_Dts', blank=True, null=True)  # Field name made lowercase.
    executiveid = models.IntegerField(db_column='ExecutiveID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LEAD'


class LeadFollowUp(models.Model):
    followupid = models.IntegerField(db_column='FollowUpID', primary_key=True)  # Field name made lowercase.
    leadid = models.ForeignKey(Lead, models.DO_NOTHING, db_column='LeadID', blank=True, null=True)  # Field name made lowercase.
    executiveid = models.IntegerField(db_column='ExecutiveID', blank=True, null=True)  # Field name made lowercase.
    actiontaken = models.CharField(db_column='ActionTaken', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    remarks = models.TextField(db_column='Remarks', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    leadstatusid = models.ForeignKey('LeadStatus', models.DO_NOTHING, db_column='LeadStatusID', blank=True, null=True)  # Field name made lowercase.
    followupdate = models.DateField(db_column='FollowUpDate', blank=True, null=True)  # Field name made lowercase.
    added_by = models.CharField(db_column='Added_By', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_dts = models.DateTimeField(db_column='Added_Dts', blank=True, null=True)  # Field name made lowercase.
    executive_name = models.CharField(db_column='Executive_Name', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LEAD_FOLLOW_UP'


class LeadSource(models.Model):
    leadsourceid = models.IntegerField(db_column='LeadSourceID', primary_key=True)  # Field name made lowercase.
    leadsourcename = models.CharField(db_column='LeadSourceName', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.CharField(db_column='Added_By', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_dts = models.DateTimeField(db_column='Added_Dts', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LEAD_SOURCE'


class LeadStatus(models.Model):
    statusid = models.IntegerField(db_column='StatusID', primary_key=True)  # Field name made lowercase.
    statusname = models.CharField(db_column='StatusName', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.CharField(db_column='Added_By', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_dts = models.DateTimeField(db_column='Added_Dts', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LEAD_STATUS'


class Product(models.Model):
    productid = models.IntegerField(db_column='ProductID', primary_key=True)  # Field name made lowercase.
    productname = models.CharField(db_column='ProductName', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    categoryid = models.ForeignKey('ProductCategory', models.DO_NOTHING, db_column='CategoryID', blank=True, null=True)  # Field name made lowercase.
    is_active = models.SmallIntegerField(db_column='Is_Active', blank=True, null=True)  # Field name made lowercase.
    added_by = models.CharField(db_column='Added_By', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_dts = models.DateTimeField(db_column='Added_Dts', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PRODUCT'


class ProductCategory(models.Model):
    categoryid = models.IntegerField(db_column='CategoryID', primary_key=True)  # Field name made lowercase.
    categoryname = models.CharField(db_column='CategoryName', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.CharField(db_column='Added_By', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_dts = models.DateTimeField(db_column='Added_Dts', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PRODUCT_CATEGORY'


class Region(models.Model):
    regionid = models.IntegerField(db_column='RegionID', primary_key=True)  # Field name made lowercase.
    regionname = models.CharField(db_column='RegionName', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.CharField(db_column='Added_By', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_dts = models.DateTimeField(db_column='Added_Dts', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REGION'


class Territory(models.Model):
    territoryid = models.IntegerField(db_column='TerritoryID', primary_key=True)  # Field name made lowercase.
    territoryname = models.CharField(db_column='TerritoryName', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    regionid = models.ForeignKey(Region, models.DO_NOTHING, db_column='RegionID', blank=True, null=True)  # Field name made lowercase.
    added_by = models.CharField(db_column='Added_By', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_dts = models.DateTimeField(db_column='Added_Dts', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TERRITORY'
