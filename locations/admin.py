from django.contrib import admin
from .models import Region, Department, Commune

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code")
    search_fields = ("name", "code")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "region", "code")
    search_fields = ("name", "code", "region__name")
    list_filter = ("region",)


@admin.register(Commune)
class CommuneAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "department", "code")
    search_fields = ("name", "code", "department__name", "department__region__name")
    list_filter = ("department__region", "department")
