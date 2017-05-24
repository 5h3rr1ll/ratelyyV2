from django.contrib import admin

from .models import Concern, Company, Brand, Product

# Register your models here.
admin.site.register(Concern)
admin.site.register(Company)
admin.site.register(Brand)
admin.site.register(Product)
