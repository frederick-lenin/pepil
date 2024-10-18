from django.contrib import admin
from App.models import CustomUser, Category, Product


# Register your models here.

admin.site.register(Category)
admin.site.register(CustomUser)