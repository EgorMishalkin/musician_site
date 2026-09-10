from django.db import models


class Album(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    release_year = models.PositiveSmallIntegerField()
    release_type = models.CharField(max_length=20)
    accent_color = models.CharField(max_length=7)
    order = models.PositiveSmallIntegerField(default=0)

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