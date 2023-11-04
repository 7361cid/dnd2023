from django.contrib import admin
from .models import CustomClient, Product, ClassChoice

admin.site.register(CustomClient)
admin.site.register(Product)
admin.site.register(ClassChoice)
