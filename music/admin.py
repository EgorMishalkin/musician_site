from django.contrib import admin

from .models import Album, AlbumLink, ContactMessage, Single, SiteSettings, SocialLink, Track


class TrackInline(admin.TabularInline):
    model = Track
    extra = 0


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


@admin.register(Single)
class SingleAdmin(admin.ModelAdmin):
    list_display = ("title", "release_year", "order")
    list_editable = ("order",)


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "order")
    list_editable = ("order",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "subject",
        "reply_requested",
        "created_at",
    )

    readonly_fields = ("created_at",)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False