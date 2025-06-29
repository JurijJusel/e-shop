from django.contrib import admin
from .models import Order, OrderStatus
from api.carts.models import Cart
from api.customers.models import Customer


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'cart', 'amount_paid', 'created_at', 'updated_at']
    list_filter = ['customer', 'created_at']
    search_fields = ['customer__email', 'customer__phone']
    readonly_fields = ['created_at', 'updated_at', 'amount_paid']
    fieldsets = (
        (None, {'fields': ('customer', 'cart', 'amount_paid')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ['order', 'order_status', 'payment_status', 'delivery_status', 'created_at', 'updated_at']
    list_filter = ['order_status', 'payment_status', 'created_at']
    search_fields = ['order__id', 'delivery_status']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {'fields': ('order', 'order_status', 'payment_status', 'delivery_status')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
