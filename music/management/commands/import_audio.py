import json
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from music.models import Album, Single, SingleTrack, Track


MISSING_SINGLES = {
    "циклы": {
        "release_year": 2026,
        "url": "https://band.link/oAaMZ",
        "order": 0,
    },
    "интересно": {
        "release_year": 2026,
        "url": "https://band.link/rYmQt",
        "order": 1,
    },
}


class Command(BaseCommand):
    help = "Импортирует MP3 из статической версии сайта в Django media."

    def add_arguments(self, parser):
        parser.add_argument(
            "source",
            type=str,
            help="Путь к musician_site_static_working",
        )
        parser.add_argument(
            "--overwrite",
            action="store_true",
            help="Перезаписать уже импортированные аудиофайлы.",
        )

    def handle(self, *args, **options):
        source = Path(options["source"]).expanduser().resolve()
        overwrite = options["overwrite"]

        audio_root = source / "audio"
        singles_json = source / "singles_audio.json"

        if not source.exists():
            raise CommandError(f"Папка не найдена: {source}")

        if not audio_root.exists():
            raise CommandError(f"Не найдена папка audio: {audio_root}")

        if not Album.objects.exists() or not Track.objects.exists():
            raise CommandError(
                "В БД нет дискографии. Сначала выполни: "
                "py manage.py loaddata defense_data.json"
            )

        album_imported = 0
        album_skipped = 0
        album_missing = 0

        self.stdout.write("Импорт альбомов...")

        for track in Track.objects.select_related("album").order_by(
            "album__order",
            "number",
        ):
            source_file = (
                audio_root
                / track.album.slug
                / f"{track.number:02d}.mp3"
            )

            if not source_file.exists():
                album_missing += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"  нет файла: {source_file}"
                    )
                )
                continue

            if track.audio and not overwrite:
                album_skipped += 1
                continue

            if track.audio and overwrite:
                track.audio.delete(save=False)

            with source_file.open("rb") as handle:
                track.audio.save(
                    source_file.name,
                    File(handle),
                    save=True,
                )

            album_imported += 1
            self.stdout.write(
                f"  OK {track.album.title} - "
                f"{track.number:02d} {track.title}"
            )

        single_imported = 0
        single_skipped = 0
        single_missing = 0

        if not singles_json.exists():
            self.stdout.write(
                self.style.WARNING(
                    f"Не найден {singles_json}. "
                    "Синглы пропущены."
                )
            )
        else:
            self.stdout.write("Импорт синглов...")

            releases = json.loads(
                singles_json.read_text(encoding="utf-8")
            )

            for release in releases:
                release_title = release["title"]
                single = Single.objects.filter(
                    title=release_title
                ).first()

                if single is None:
                    defaults = MISSING_SINGLES.get(release_title)

                    if defaults is None:
                        self.stdout.write(
                            self.style.WARNING(
                                f"  нет Single в БД: {release_title}"
                            )
                        )
                        continue

                    single = Single.objects.create(
                        title=release_title,
                        **defaults,
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  создан релиз: {release_title}"
                        )
                    )

                for number, track_data in enumerate(
                    release.get("tracks", []),
                    start=1,
                ):
                    source_file = source / track_data["file"]

                    single_track, _ = SingleTrack.objects.update_or_create(
                        single=single,
                        number=number,
                        defaults={
                            "title": track_data["title"],
                        },
                    )

                    if not source_file.exists():
                        single_missing += 1
                        self.stdout.write(
                            self.style.WARNING(
                                f"  нет файла: {source_file}"
                            )
                        )
                        continue

                    if single_track.audio and not overwrite:
                        single_skipped += 1
                        continue

                    if single_track.audio and overwrite:
                        single_track.audio.delete(save=False)

                    with source_file.open("rb") as handle:
                        single_track.audio.save(
                            source_file.name,
                            File(handle),
                            save=True,
                        )

                    single_imported += 1
                    self.stdout.write(
                        f"  OK {release_title} - "
                        f"{track_data['title']}"
                    )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "Готово. "
                f"Альбомы: {album_imported} импортировано, "
                f"{album_skipped} уже было, "
                f"{album_missing} файлов не найдено. "
                f"Синглы: {single_imported} импортировано, "
                f"{single_skipped} уже было, "
                f"{single_missing} файлов не найдено."
            )
        )
