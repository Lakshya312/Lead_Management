from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


# =========================
# PRODUCT CATEGORY
# =========================
class Product_Category(models.Model):
    CategoryID = models.BigAutoField(primary_key=True)
    CategoryName = models.CharField(max_length=150)

    Added_By = models.CharField(max_length=100, default="system")
    Added_Dts = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Product_Category"

    def __str__(self):
        return self.CategoryName


# =========================
# PRODUCT
# =========================
class Product(models.Model):
    ProductID = models.BigAutoField(primary_key=True)
    ProductName = models.CharField(max_length=100, null=False, blank=False)

    Category = models.ForeignKey(
        Product_Category,
        on_delete=models.PROTECT,
        null=True,
        db_column="CategoryID"
    )

    Is_Active = models.BooleanField(default=True)

    Added_By = models.CharField(max_length=200)
    Added_Dts = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Product'

    def clean(self):
        if not self.ProductName:
            raise ValidationError("Product name required")

    def __str__(self):
        try:
            return self.ProductName
        except:
            return "Product"


# =========================
# REGION
# =========================
class Region(models.Model):
    RegionID = models.BigAutoField(primary_key=True)
    RegionName = models.CharField(max_length=100, null=False, blank=False)

    Added_By = models.CharField(max_length=100, default="system")
    Added_Dts = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Region"

    def clean(self):
        if not self.RegionName:
            raise ValidationError("Region name required")

    def __str__(self):
        try:
            return self.RegionName
        except:
            return "Region"


# =========================
# TERRITORY
# =========================
class Territory(models.Model):
    TerritoryID = models.BigAutoField(primary_key=True)
    TerritoryName = models.CharField(max_length=150)

    Region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        null=True,
        db_column="RegionID"
    )

    Added_By = models.CharField(max_length=100, default="system")
    Added_Dts = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Territory"

    def __str__(self):
        return self.TerritoryName


# =========================
# LEAD SOURCE
# =========================
class Lead_Source(models.Model):
    LeadSourceID = models.BigAutoField(primary_key=True)
    LeadSourceName = models.CharField(max_length=100, null=False, blank=False)

    Added_By = models.CharField(max_length=100, default="system")
    Added_Dts = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Lead_Source"

    def __str__(self):
        return self.LeadSourceName


# =========================
# LEAD STATUS
# =========================
class Lead_Status(models.Model):
    StatusID = models.BigAutoField(primary_key=True)
    StatusName = models.CharField(max_length=150)

    Added_By = models.CharField(max_length=100, default="system")
    Added_Dts = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Lead_Status"

    def __str__(self):
        return self.StatusName


# =========================
# LEAD
# =========================
class Lead(models.Model):
    LeadID = models.BigAutoField(primary_key=True)

    PersonName = models.CharField(max_length=100, null=False, blank=False)

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    Gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        null=True,
        blank=True
    )

    CompanyName = models.CharField(max_length=200, null=True, blank=True)
    ContactNo = models.CharField(max_length=20, null=True, blank=True)

    Email = models.EmailField(max_length=150, null=True, blank=True)

    City = models.CharField(max_length=100, null=True, blank=True)
    State = models.CharField(max_length=100, null=True, blank=True)

    Territory = models.ForeignKey(
        "Territory",
        on_delete=models.PROTECT,
        null=True,
        db_column="TerritoryID"
    )

    Region = models.ForeignKey(Region, on_delete=models.PROTECT, null=True, db_column="RegionID")
    Product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True, db_column="ProductID")
    Status = models.ForeignKey(Lead_Status, on_delete=models.PROTECT, null=True, db_column="StatusID")

    Source = models.ForeignKey(Lead_Source, on_delete=models.PROTECT, null=True, db_column="LeadSourceID")

    BusinessNeed = models.TextField(null=True, blank=True)

    Lead_Gen_Date = models.DateTimeField(null=True, blank=True)

    Added_By = models.CharField(max_length=100, default="system")
    Added_Dts = models.DateTimeField(auto_now_add=True)

    ExecutiveID = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "Lead"

    def clean(self):
        if not self.PersonName:
            raise ValidationError("Person name required")

        if self.ContactNo:
            if not self.ContactNo.isdigit():
                raise ValidationError("Contact number must be digit only")

            if len(self.ContactNo) != 10:
                raise ValidationError("Contact number 10 digit required")

        if self.Email:
            if not self.Email.endswith(".com"):
                raise ValidationError("Email .com required")

    def __str__(self):
        try:
            return self.PersonName
        except:
            return "Lead"


# =========================
# LEAD FOLLOW UP
# =========================
class Lead_Follow_Up(models.Model):
    FollowUpID = models.BigAutoField(primary_key=True)

    Lead = models.ForeignKey(Lead, on_delete=models.CASCADE, db_column="LeadID")

    ExecutiveID = models.IntegerField(null=True, blank=True)


    ActionTaken = models.CharField(max_length=100, null=True, blank=True)
    Remarks = models.TextField(null=True, blank=True)

    LeadStatus = models.ForeignKey(
        Lead_Status,
        on_delete=models.PROTECT,
        null=True,
        db_column="LeadStatusID"
    )

    FollowUpDate = models.DateTimeField()

    Added_By = models.CharField(max_length=100, default="system")
    Added_Dts = models.DateTimeField(auto_now_add=True)

    Executive_Name = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        db_table = "Lead_Follow_Up"

    def __str__(self):
        try:
            return f"FollowUp - {self.Lead.PersonName}"
        except:
            return "FollowUp"

# =========================
# ROLE BASED ACCESS CONTROL
# =========================
class UserProfile(models.Model):
     ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Executive', 'Executive'),
     )

     user = models.OneToOneField(User, on_delete=models.CASCADE)
     role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='Executive'
     )

     is_main_admin = models.BooleanField(default=False)

     def __str__(self):
        return f"{self.user.username} - {self.role}"

