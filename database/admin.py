from django.contrib import admin

from .models import Concerns, Companies, Brands, Products

# Register your models here.
admin.site.register(Concerns)
admin.site.register(Companies)
admin.site.register(Brands)
admin.site.register(Products)
