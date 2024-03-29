from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Roles)
admin.site.register(UserRole)
admin.site.register(Organizations)
admin.site.register(Category)
admin.site.register(OrganizationCategory)
admin.site.register(Charges)
admin.site.register(OrganizationCharges)
admin.site.register(Turns)

