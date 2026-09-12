from django.core.management.base import BaseCommand

from music.models import Album, AlbumLink, Single, Track


class Command(BaseCommand):
    help = "Load honeysuckler discography into the database"

    def handle(self, *args, **options):
        discography = [
            {
                "title": "питерский альбом",
                "slug": "piterskij-albom",
                "release_year": 2026,
                "release_type": "album",
                "accent_color": "#d20d29",
                "order": 0,
                "cover": "covers/cover.png",
                "tracks": [
                    (1, "палмер", "4:12"),
                    (2, "реп", "2:53"),
                    (3, "факбой 2", "1:31"),
                    (4, "выходной", "3:18"),
                    (5, "на пати", "2:24"),
                    (6, "капитал", "2:20"),
                    (7, "однажды", "3:47"),
                    (8, "фрагменты", "5:18"),
                    (9, "факбой 2 2", "1:31"),
                ],
                "links": [
                    (
                        "youtube",
                        "https://www.youtube.com/playlist?list=OLAK5uy_my_R4vKK4NVa4GTJnxGiVyLXKdrgv3Ij4",
                        0,
                    ),
                    (
                        "яндекс музыка",
                        "https://music.yandex.ru/album/42914910?utm_source=web&utm_medium=copy_link",
                        1,
                    ),
                    (
                        "spotify",
                        "https://open.spotify.com/album/6wfuN6AisTMFs0A8jnpruF?si=J_3JodW5Se-bgl1V6ui-1g",
                        2,
                    ),
                ],
            },
            {
                "title": "ништяк музыка",
                "slug": "nishtyak-muzyka",
                "release_year": 2026,
                "release_type": "ep",
                "accent_color": "#7CFF6B",
                "order": 1,
                "cover": "covers/691ae11f-0ddd-4d51-9b03-f4bc52007c5b.jpg",
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
                "cover": "covers/image.png",
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
                "cover": "covers/neo_emo_by_хонисаклер.jpg",
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
                "cover": "covers/photo_5368551095724529477_y.jpg",
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
                "cover": "covers/photo_5472401794329073668_y.jpg",
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
            tracks = album_data.get("tracks", [])
            links = album_data.get("links", [])

            album_defaults = {
                key: value
                for key, value in album_data.items()
                if key not in ("tracks", "links")
            }

            album, _ = Album.objects.update_or_create(
                slug=album_data["slug"],
                defaults=album_defaults,
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

            for name, url, order in links:
                AlbumLink.objects.update_or_create(
                    album=album,
                    name=name,
                    defaults={
                        "url": url,
                        "order": order,
                    },
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

        self.stdout.write(
            self.style.SUCCESS("Discography loaded successfully")
        )