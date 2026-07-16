from django.contrib import admin
from .models import SDG, SDGTarget, SDGIndicator


@admin.register(SDG)
class SDGAdmin(admin.ModelAdmin):
    list_display = ("number", "name", "color")
    search_fields = ("name",)


@admin.register(SDGTarget)
class SDGTargetAdmin(admin.ModelAdmin):
    list_display = ("code", "sdg", "description")
    search_fields = ("code", "description")
    list_filter = ("sdg",)


@admin.register(SDGIndicator)
class SDGIndicatorAdmin(admin.ModelAdmin):
    list_display = ("code", "target", "unit", "frequency")
    list_editable = ("unit", "frequency")
    list_filter = ("frequency", "target__sdg")
    search_fields = ("code", "description")
