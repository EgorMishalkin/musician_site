from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),

    path(
        "audio/album/<int:pk>/",
        views.stream_album_track,
        name="stream_album_track",
    ),
    path(
        "audio/single/<int:pk>/",
        views.stream_single_track,
        name="stream_single_track",
    ),

    path(
        "download/track/album/<int:pk>/",
        views.download_album_track,
        name="download_album_track",
    ),
    path(
        "download/track/single/<int:pk>/",
        views.download_single_track,
        name="download_single_track",
    ),
    path(
        "download/album/<slug:slug>/",
        views.download_album,
        name="download_album",
    ),
]
