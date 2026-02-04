from django.contrib import admin
from .models import FidsDetail

@admin.register(FidsDetail)
class FidsDetailAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'ip_address', 'mac_address', 'location')
    search_fields = ('device_id', 'ip_address', 'mac_address', 'location')
    list_filter = ('location',)
