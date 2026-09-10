from django.shortcuts import render

from .models import Album


def home(request):
    album = Album.objects.first()

    return render(
        request,
        "music/home.html",
        {
            "album": album,
        },
    )