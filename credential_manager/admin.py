from django.contrib import admin
from .models import System, Credential, Location

@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')
    search_fields = ('name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')
    search_fields = ('name',)

@admin.register(Credential)
class CredentialAdmin(admin.ModelAdmin):
    list_display = ('system', 'location', 'description', 'username', 'ipv4', 'updated')
    list_filter = ('system', 'location', 'created', 'updated')
    search_fields = ('description', 'username', 'ipv4', 'remarks')
    readonly_fields = ('created', 'updated')
