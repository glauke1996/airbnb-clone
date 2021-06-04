from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.RoomType, models.Amenity, models.Facility, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """Item Admin Definition"""

    pass


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """Room Admin Definition"""

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "check_in",
        "check_out",
    )
    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
    )
    search_fields = [
        "city",
        "host__username",
    ]
    filter_horizontal = (
        "amenity",
        "facility",
        "house_rule",
    )
    fieldsets = (
        (
            "Basic  Info",
            {"fields": ("name", "description", "country", "city", "address", "price")},
        ),
        ("Time", {"fields": ("check_in", "check_out", "instant_book")}),
        ("Room", {"fields": ("beds", "bedrooms", "bath", "guests")}),
        (
            "More about the room",
            {
                "classes": ("collapse",),
                "fields": ("room_type", "amenity", "facility", "house_rule"),
            },
        ),
        (
            "Last Detail",
            {
                "classes": ("collapse",),
                "fields": ("host",),
            },
        ),
    )
    ordering = ("name",)

    def count_amenities(self, obj):
        return "potato"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Photo Admin Definition"""

    pass
