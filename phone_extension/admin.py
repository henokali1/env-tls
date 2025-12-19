from django.contrib import admin
from .models import PhoneExtension

@admin.register(PhoneExtension)
class PhoneExtensionAdmin(admin.ModelAdmin):
    list_display = ('name', 'extension_number', 'full_number')
    search_fields = ('name', 'extension_number')
