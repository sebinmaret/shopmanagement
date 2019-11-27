from django.contrib import admin
from Shop.models import Employee,LogRecord,SalesRecord,Supplier,SupplierCat,ExpiryDetails,Products,Sale
# Register your models here.
admin.site.register(Employee)
admin.site.register(LogRecord)
admin.site.register(SalesRecord)
admin.site.register(SupplierCat)
admin.site.register(Supplier)
admin.site.register(Products)
admin.site.register(ExpiryDetails)
admin.site.register(Sale)

