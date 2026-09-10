from django.contrib import admin

from .models import Album, Track


class TrackInline(admin.TabularInline):
    model = Track
    extra = 1


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "release_year", "release_type", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [TrackInline]


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("number", "title", "album", "duration")
    list_filter = ("album",)
    ordering = ("album", "number")