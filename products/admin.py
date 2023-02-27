from django.contrib import admin

from .models import Product, Category, CartItem

admin.site.register(Category)
admin.site.register(CartItem)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    raw_id_fields = ('category',)
