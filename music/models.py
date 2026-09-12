from django.db import models
from django.core.exceptions import ValidationError

class Album(models.Model):
    class ReleaseType(models.TextChoices):
        ALBUM = "album", "Альбом"
        EP = "ep", "Мини-альбом"

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    release_year = models.PositiveSmallIntegerField()

    release_type = models.CharField(
        max_length=20,
        choices=ReleaseType.choices,
    )

    accent_color = models.CharField(max_length=7)
    order = models.PositiveSmallIntegerField(default=0)
    cover = models.ImageField(upload_to="covers/", blank=True)
    upc = models.CharField(
        max_length=20,
        blank=True,
        unique=True,
        null=True,
    )

    def __str__(self):
        return self.title

class Track(models.Model):
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name="tracks",
    )
    number = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=100)
    duration = models.CharField(max_length=10)

    class Meta:
        ordering = ["number"]

        constraints = [
            models.UniqueConstraint(
                fields=["album", "number"],
                name="unique_track_number_per_album",
            ),
        ]

    def __str__(self):
        return f"{self.number}. {self.title}"


class Single(models.Model):
    title = models.CharField(max_length=100)
    release_year = models.PositiveSmallIntegerField()
    url = models.URLField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class AlbumLink(models.Model):
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name="links",
    )
    name = models.CharField(max_length=50)
    url = models.URLField()
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

        constraints = [
            models.UniqueConstraint(
                fields=["album", "name"],
                name="unique_service_per_album",
            ),
        ]

    def __str__(self):
        return f"{self.album.title} — {self.name}"

class SocialLink(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    class Subject(models.TextChoices):
        MUSIC = "music", "Музыка"
        COLLAB = "collab", "Сотрудничество"
        OTHER = "other", "Другое"

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(
        max_length=20,
        choices=Subject.choices,
    )
    message = models.TextField()
    reply_requested = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.email}"


class SiteSettings(models.Model):
    artist_photo = models.ImageField(
        upload_to="photos/",
        blank=True,
    )

    def __str__(self):
        return "Настройки сайта"


class MaterialLink(models.Model):
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name="materials",
        blank=True,
        null=True,
    )

    single = models.ForeignKey(
        Single,
        on_delete=models.CASCADE,
        related_name="materials",
        blank=True,
        null=True,
    )

    title = models.CharField(max_length=150)
    url = models.URLField()
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def clean(self):
        if bool(self.album) == bool(self.single):
            raise ValidationError(
                "Материал должен относиться либо к альбому, либо к синглу."
            )

    def __str__(self):
        release = self.album or self.single
        return f"{release} — {self.title}"