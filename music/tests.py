from django.test import TestCase
from django.urls import reverse

from .models import Album, ContactMessage


class HomeViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first_album = Album.objects.create(
            title="ништяк музыка",
            slug="nishtyak-muzyka",
            release_year=2026,
            release_type="ep",
            accent_color="#7CFF6B",
            order=1,
        )

        cls.neo_emo = Album.objects.create(
            title="neo emo",
            slug="neo-emo",
            release_year=2024,
            release_type="ep",
            accent_color="#2457FF",
            order=2,
        )

    def test_album_can_be_selected_with_get_parameter(self):
        response = self.client.get(
            reverse("home"),
            {"album": "neo-emo"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["selected_album"],
            self.neo_emo,
        )

    def test_last_album_is_loaded_from_cookie(self):
        self.client.cookies["last_album"] = "neo-emo"

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["selected_album"],
            self.neo_emo,
        )

    def test_valid_contact_form_creates_message(self):
        response = self.client.post(
            reverse("home"),
            {
                "name": "Егор",
                "email": "test@example.com",
                "subject": "music",
                "message": "Тестовое сообщение",
                "reply_requested": True,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactMessage.objects.count(), 1)

        message = ContactMessage.objects.first()

        self.assertEqual(message.name, "Егор")
        self.assertEqual(message.email, "test@example.com")
        self.assertEqual(message.message, "Тестовое сообщение")

    def test_unknown_album_returns_404(self):
        response = self.client.get(
            reverse("home"),
            {"album": "album-does-not-exist"},
        )

        self.assertEqual(response.status_code, 404)