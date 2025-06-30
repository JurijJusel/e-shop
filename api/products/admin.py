from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'created_at', 'updated_at']
    list_filter = ['price', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {'fields': ('name', 'description', 'price', 'image')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
