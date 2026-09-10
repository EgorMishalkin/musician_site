from django.core.management.base import BaseCommand

from music.models import Album, Single, Track


class Command(BaseCommand):
    help = "Load honeysuckler discography into the database"

    def handle(self, *args, **options):
        discography = [
            {
                "title": "ништяк музыка",
                "slug": "nishtyak-muzyka",
                "release_year": 2026,
                "release_type": "ep",
                "accent_color": "#7CFF6B",
                "order": 1,
                "tracks": [
                    (1, "дуралеи", "2:15"),
                    (2, "ништяк музыка", "1:56"),
                    (3, "хонибургер 2", "2:19"),
                    (4, "детка 0_0", "2:03"),
                ],
            },
            {
                "title": "ништяк музик",
                "slug": "nishtyak-muzik",
                "release_year": 2025,
                "release_type": "ep",
                "accent_color": "#B6FF00",
                "order": 2,
                "tracks": [
                    (1, "шмоук", "2:20"),
                    (2, "ништяк music", "1:57"),
                    (3, "хонибургер", "2:19"),
                    (4, "бейби ^_^", "2:01"),
                ],
            },
            {
                "title": "neo emo",
                "slug": "neo-emo",
                "release_year": 2024,
                "release_type": "ep",
                "accent_color": "#2457FF",
                "order": 3,
                "tracks": [
                    (1, "пережить", "2:10"),
                    (2, "бездарность", "2:01"),
                    (3, "boyfriend XD", "4:20"),
                    (4, "сколько?", "2:27"),
                    (5, "вера", "2:27"),
                ],
            },
            {
                "title": "слабый персонаж",
                "slug": "slabyy-personazh",
                "release_year": 2023,
                "release_type": "album",
                "accent_color": "#FF3B30",
                "order": 4,
                "tracks": [
                    (1, "опенинг", "2:17"),
                    (2, "драться!", "2:05"),
                    (3, "бояться", "2:17"),
                    (4, "слабый персонаж", "3:00"),
                    (5, "бич пакет", "2:58"),
                    (6, "молодым и злым", "2:18"),
                    (7, "о свободе", "2:03"),
                    (8, "пазла", "2:47"),
                    (9, "трудности", "2:50"),
                    (10, "воронка", "2:59"),
                    (11, "я не знаю", "2:10"),
                    (12, "искры", "3:12"),
                    (13, "гербарий 2", "2:37"),
                    (14, "прощай", "3:03"),
                ],
            },
            {
                "title": "sad boys club",
                "slug": "sad-boys-club",
                "release_year": 2022,
                "release_type": "album",
                "accent_color": "#D4A800",
                "order": 5,
                "tracks": [
                    (1, "интро", "0:53"),
                    (2, "додик", "3:00"),
                    (3, "sad boys club", "2:21"),
                    (4, "я хочу", "2:36"),
                    (5, "5 минут", "2:34"),
                    (6, "лин лин лин", "1:54"),
                    (7, "солевая стейси", "2:39"),
                ],
            },
        ]

        for album_data in discography:
            tracks = album_data.pop("tracks")

            album, _ = Album.objects.update_or_create(
                slug=album_data["slug"],
                defaults=album_data,
            )

            for number, title, duration in tracks:
                Track.objects.update_or_create(
                    album=album,
                    number=number,
                    defaults={
                        "title": title,
                        "duration": duration,
                    },
                )

        self.stdout.write(
            self.style.SUCCESS("Discography loaded successfully")
        )

        singles = [
            ("fomo", 2026, 1),
            ("hangover (x__x)", 2026, 2),
            ("2023 ^_^", 2026, 3),
            ("расскажи ^_^", 2026, 4),
            ("баллада об оппчике", 2025, 5),
            ("mlg moment", 2025, 6),
            ("егор привет", 2025, 7),
            ("не умею...", 2024, 8),
            ("ты ты ты", 2024, 9),
            ("паранойя!", 2023, 10),
            ("качели", 2023, 11),
            ("3", 2023, 12),
        ]

        for title, year, order in singles:
            Single.objects.update_or_create(
                title=title,
                defaults={
                    "release_year": year,
                    "order": order,
                },
            )