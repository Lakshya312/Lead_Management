from django.db import models

class Region(models.Model):
    """
    Master lookup schema for geographical operational regions.
    """

    regionid = models.AutoField(primary_key=True, db_column='regionid')
    regionname = models.CharField(max_length=150, unique=True, db_column='regionname')
    added_by = models.CharField(max_length=100, blank=True, null=True, db_column='added_by')
    added_dts = models.CharField(max_length=100, blank=True, null=True, db_column='added_dts')

    class Meta:
        db_table = 'tbl_region_master'

    def __str__(self):
        return self.regionname


class ProductCategory(models.Model):
    """
    Master lookup schema for segregating corporate enterprise product segments.
    """
    categoryid = models.AutoField(primary_key=True, db_column='categoryid')
    categoryname = models.CharField(max_length=150, unique=True, db_column='categoryname')
    added_by = models.CharField(max_length=100, blank=True, null=True, db_column='added_by')
    added_dts = models.CharField(max_length=100, blank=True, null=True, db_column='added_dts')

    class Meta:
        db_table = 'tbl_product_category_master'

    def __str__(self):
        return self.categoryname


class LeadSource(models.Model):
    """
    Master lookup schema for tracking the inbound origin channels of business leads.
    """
    leadsourceid = models.AutoField(primary_key=True, db_column='leadsourceid')
    leadsourcename = models.CharField(max_length=150, unique=True, db_column='leadsourcename')
    added_by = models.CharField(max_length=100, blank=True, null=True, db_column='added_by')
    added_dts = models.CharField(max_length=100, blank=True, null=True, db_column='added_dts')

    class Meta:
        db_table = 'tbl_lead_source_master'

    def __str__(self):
        return self.leadsourcename


class LeadStatus(models.Model):
    """
    Master lookup schema defining state cycles in the marketing pipeline matrix.
    """
    statusid = models.AutoField(primary_key=True, db_column='statusid')
    statusname = models.CharField(max_length=150, unique=True, db_column='statusname')
    added_by = models.CharField(max_length=100, blank=True, null=True, db_column='added_by')
    added_dts = models.CharField(max_length=100, blank=True, null=True, db_column='added_dts')

    class Meta:
        db_table = 'tbl_lead_status_master'

    def __str__(self):
        return self.statusname


class Territory(models.Model):
    """
    Operational tracking sectors linked structurally to regional centers.
    """
    territoryid = models.AutoField(primary_key=True, db_column='territoryid')
    territoryname = models.CharField(max_length=150, db_column='territoryname')
    regionid = models.ForeignKey(Region, on_delete=models.PROTECT, db_column='regionid')
    added_by = models.CharField(max_length=100, blank=True, null=True, db_column='added_by')
    added_dts = models.CharField(max_length=100, blank=True, null=True, db_column='added_dts')

    class Meta:
        db_table = 'tbl_territory_master'

    def __str__(self):
        return self.territoryname


class Product(models.Model):
    """
    Corporate inventory item tracking catalogs associated with business branches.
    """
    productid = models.AutoField(primary_key=True, db_column='productid')
    productname = models.CharField(max_length=150, db_column='productname')
    categoryid = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, db_column='categoryid')
    is_active = models.IntegerField(default=1, db_column='is_active')
    added_by = models.CharField(max_length=100, blank=True, null=True, db_column='added_by')
    added_dts = models.CharField(max_length=100, blank=True, null=True, db_column='added_dts')

    class Meta:
        db_table = 'tbl_product_master'

    def __str__(self):
        return self.productname


class Lead(models.Model):
    """
    Core business lead engine schema handling relational tracking configurations.
    """
    leadid = models.AutoField(primary_key=True, db_column='leadid')
    personname = models.CharField(max_length=150, db_column='personname')
    gender = models.CharField(max_length=50, blank=True, null=True, db_column='gender')
    companyname = models.CharField(max_length=200, blank=True, null=True, db_column='companyname')
    contactno = models.CharField(max_length=50, blank=True, null=True, db_column='contactno')
    email = models.EmailField(max_length=150, blank=True, null=True, db_column='email')
    city = models.CharField(max_length=100, blank=True, null=True, db_column='city')
    state = models.CharField(max_length=100, blank=True, null=True, db_column='state')
    territoryid = models.ForeignKey(Territory, on_delete=models.PROTECT, db_column='territoryid')
    regionid = models.ForeignKey(Region, on_delete=models.PROTECT, db_column='regionid')
    productid = models.ForeignKey(Product, on_delete=models.PROTECT, db_column='productid')
    statusid = models.ForeignKey(LeadStatus, on_delete=models.PROTECT, db_column='statusid')
    leadsourceid = models.ForeignKey(LeadSource, on_delete=models.PROTECT, db_column='leadsourceid')
    businessneed = models.TextField(blank=True, null=True, db_column='businessneed')
    lead_gen_date = models.DateField(blank=True, null=True, db_column='lead_gen_date')
    added_by = models.CharField(max_length=100, blank=True, null=True, db_column='added_by')
    added_dts = models.CharField(max_length=100, blank=True, null=True, db_column='added_dts')
    executiveid = models.IntegerField(db_column='executiveid')

    class Meta:
        db_table = 'tbl_lead_pipeline'

    def __str__(self):
        return f"{self.personname} - {self.companyname}"


class LeadFollowUp(models.Model):
    """
    Transactional execution history log mapping dynamic lead status transformations.
    """
    followupid = models.AutoField(primary_key=True, db_column='followupid')
    leadid = models.ForeignKey(Lead, on_delete=models.PROTECT, db_column='leadid')
    executiveid = models.IntegerField(db_column='executiveid')
    actiontaken = models.CharField(max_length=255, db_column='actiontaken')
    remarks = models.TextField(blank=True, null=True, db_column='remarks')
    leadstatusid = models.ForeignKey(LeadStatus, on_delete=models.PROTECT, db_column='leadstatusid')
    followupdate = models.DateField(blank=True, null=True, db_column='followupdate')
    added_by = models.CharField(max_length=100, blank=True, null=True, db_column='added_by')
    added_dts = models.CharField(max_length=100, blank=True, null=True, db_column='added_dts')
    executive_name = models.CharField(max_length=150, blank=True, null=True, db_column='executive_name')

    class Meta:
        db_table = 'tbl_lead_followup_history'

    def __str__(self):
        return f"FollowUp {self.followupid} for Lead {self.leadid_id}"