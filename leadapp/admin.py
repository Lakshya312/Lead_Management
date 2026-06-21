from django.contrib import admin
from .models import *

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Region)
admin.site.register(Territory)
admin.site.register(Lead)
admin.site.register(LeadStatus)
admin.site.register(LeadSource)
admin.site.register(LeadFollowUp)