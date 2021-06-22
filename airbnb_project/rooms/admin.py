from django.contrib import admin
from django.utils.html import mark_safe
from . import models

# Register your models here.


@admin.register(models.RoomType, models.Amenity, models.Facility, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """Item Admin Definition"""

    # list_display = (
    #     "name",
    #     "used_by",
    # )

    # def used_by(self, obj):
    #     return obj.rooms.count()
    pass


class PhotoInLine(admin.TabularInline):
    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """Room Admin Definition"""

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        print(obj.user)
        super().save_model(request, obj, form, change)

    inlines = [
        PhotoInLine,  # foreign key converse
    ]

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "check_in",
        "check_out",
        "total_rating",
    )
    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
    )
    raw_id_fields = ("host",)
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

    # def count_amenities(self, obj):
    #     return obj.Amenity.count()

    # def count_photos(self, obj):
    #     return obj.Photo.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Photo Admin Definition"""

    list_display = (
        "__str__",
        "get_thumbnail",
    )

    def get_thumbnail(self, obj):
        # obj's not just a string but Class(obj)
        return mark_safe(f"<img src={obj.file.url} width=100px height=100px/>")

    get_thumbnail.short_description = "thumbnail"
