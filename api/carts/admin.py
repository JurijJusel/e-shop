from django.contrib import admin
from .models import Cart
from api.products.models import Product
from api.customers.models import Customer


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'total_price', 'created_at', 'updated_at']
    list_filter = ['customer', 'created_at']
    search_fields = ['customer__email', 'customer__phone']
    readonly_fields = ['created_at', 'updated_at', 'total_price']
    filter_horizontal = ['products']
    fieldsets = (
        (None, {'fields': ('customer', 'products')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
        ('Information', {'fields': ('total_price',)}),
    )
