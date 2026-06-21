from django.db import models
from django.utils import timezone

class ProductCategory(models.Model):
    CategoryID = models.IntegerField(primary_key=True)
    CategoryName = models.CharField(max_length=200)

    Added_By = models.CharField(max_length=100, blank=True)
    Added_Dts = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.CategoryName

class Region(models.Model):
    RegionID = models.AutoField(primary_key=True)
    RegionName = models.CharField(max_length=100)

    Added_By = models.CharField(max_length=100, blank=True)
    Added_Dts = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.RegionName


class Product(models.Model):
    ProductID = models.AutoField(primary_key=True)

    ProductName = models.CharField(max_length=200)

    CategoryID = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        db_column="CategoryID"
    )

    Is_Active = models.BooleanField(default=True)

    Added_By = models.CharField(max_length=100, blank=True)
    Added_Dts = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.ProductName



class Territory(models.Model):
    TerritoryID = models.IntegerField(primary_key=True)

    TerritoryName = models.CharField(max_length=200)

    RegionID = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        db_column="RegionID"
    )

    Added_By = models.CharField(max_length=100, blank=True)
    Added_Dts = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.TerritoryName

class LeadStatus(models.Model):
    StatusID = models.IntegerField(primary_key=True)

    StatusName = models.CharField(max_length=100)

    Added_By = models.CharField(max_length=100, blank=True)
    Added_Dts = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.StatusName


class LeadSource(models.Model):
    LeadSourceID = models.IntegerField(primary_key=True)

    LeadSourceName = models.CharField(max_length=100)

    Added_By = models.CharField(max_length=100, blank=True)
    Added_Dts = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.LeadSourceName


class Lead(models.Model):
    LeadID = models.AutoField(primary_key=True)

    PersonName = models.CharField(max_length=200)

    Gender = models.CharField(max_length=20)

    CompanyName = models.CharField(max_length=200)

    ContactNo = models.CharField(max_length=20)

    Email = models.EmailField()

    City = models.CharField(max_length=100)

    State = models.CharField(max_length=100)

    TerritoryID = models.ForeignKey(
        Territory,
        on_delete=models.CASCADE,
        db_column="TerritoryID"
    )

    RegionID = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        db_column="RegionID"
    )

    ProductID = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        db_column="ProductID"
    )

    StatusID = models.ForeignKey(
        LeadStatus,
        on_delete=models.CASCADE,
        db_column="StatusID"
    )

    LeadSourceID = models.ForeignKey(
        LeadSource,
        on_delete=models.CASCADE,
        db_column="LeadSourceID"
    )

    BusinessNeed = models.TextField()

    Lead_Gen_Date = models.DateField()

    ExecutiveID = models.IntegerField()

    Added_By = models.CharField(max_length=100, blank=True)
    Added_Dts = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.PersonName

class LeadFollowUp(models.Model):
    FollowUpID = models.IntegerField(primary_key=True)

    LeadID = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        db_column="LeadID"
    )

    ExecutiveID = models.IntegerField()

    ActionTaken = models.TextField()

    Remarks = models.TextField()

    LeadStatusID = models.ForeignKey(
        LeadStatus,
        on_delete=models.CASCADE,
        db_column="LeadStatusID"
    )

    FollowUpDate = models.DateField()

    Executive_Name = models.CharField(max_length=200)

    Added_By = models.CharField(max_length=100, blank=True)
    Added_Dts = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.FollowUpID)