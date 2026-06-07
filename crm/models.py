from django.db import models


class Product(models.Model):
    productid = models.IntegerField(db_column='ProductID', primary_key=True)  # Field name made lowercase.
    productname = models.CharField(db_column='ProductName', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    categoryid = models.ForeignKey('ProductCategory', models.DO_NOTHING, db_column='CategoryID', blank=True, null=True)  # Field name made lowercase.
    is_active = models.SmallIntegerField(db_column='Is_Active', blank=True, null=True)  # Field name made lowercase.
    added_by = models.CharField(db_column='Added_By', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_dts = models.DateTimeField(db_column='Added_Dts', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Product'


class ProductCategory(models.Model):
    categoryid = models.IntegerField(db_column='CategoryID', primary_key=True)  # Field name made lowercase.
    categoryname = models.CharField(db_column='CategoryName', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.CharField(db_column='Added_By', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_dts = models.TimeField(db_column='Added_Dts', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Product_Category'


class Region(models.Model):
    regionid = models.IntegerField(db_column='RegionID', primary_key=True)  # Field name made lowercase.
    regionname = models.CharField(db_column='RegionName', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_by = models.CharField(db_column='Added_By', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    added_dts = models.TimeField(db_column='Added_Dts', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Region'