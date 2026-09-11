from django.core.management.base import BaseCommand

from music.models import Album, AlbumLink
from music.services.release_lookup import lookup_release


class Command(BaseCommand):
    help = "Find UPC and streaming links for all albums"

    def handle(self, *args, **options):
        albums = Album.objects.all()

        for album in albums:
            self.stdout.write(f"Поиск: {album.title}")

            result = lookup_release(album.title)

            upc = result.get("upc")

            if upc:
                album.upc = upc
                album.save(update_fields=["upc"])

                self.stdout.write(
                    self.style.SUCCESS(f"UPC найден: {upc}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING("UPC не найден")
                )

            links = result.get("links", {})

            for name, url in links.items():
                if not url:
                    continue

                AlbumLink.objects.update_or_create(
                    album=album,
                    name=name,
                    defaults={
                        "url": url,
                    },
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"{name}: {url}"
                    )
                )

            self.stdout.write("")