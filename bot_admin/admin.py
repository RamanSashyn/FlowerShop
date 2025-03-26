from django.contrib import admin
from .models import Bouquet, Order


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "occasion")
    search_fields = ("name", "flowers", "description")
    list_filter = ("occasion",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "telegram_username", "phone", "delivery_date", "status")
    search_fields = ("customer_name", "telegram_username", "address")
    list_filter = ("status", "delivery_date")
    readonly_fields = ("created_at",)