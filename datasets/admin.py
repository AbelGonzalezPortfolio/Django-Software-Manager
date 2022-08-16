from django.contrib import admin
from . import models


@admin.action(description="Sync")
def sync(modeladmin, request, queryset):
    queryset.update_ip()
    queryset.update_network_status()
    queryset.update_remoting_status()
    queryset.update_software()


class ComputerAdmin(admin.ModelAdmin):
    list_display = ["hostname", "status", "ip"]
    ordering = ["hostname"]
    search_fields = ["hostname"]
    actions = [sync]


class SoftwareAdmin(admin.ModelAdmin):
    list_display = ["name", "version"]
    ordering = ["name"]
    search_fields = ["name"]


# Register your models here.
admin.site.register(models.Computer, ComputerAdmin)
admin.site.register(models.Software, SoftwareAdmin)
