from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_id', 'email', 'phone', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['customer_id', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {'fields': ('customer_id', 'phone', 'email', 'address')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
