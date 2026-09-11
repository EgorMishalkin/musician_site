from django.shortcuts import get_object_or_404, render

from .models import Album, Single, SocialLink

def home(request):
    albums = Album.objects.prefetch_related("tracks").order_by("order")

    selected_slug = request.GET.get("album")

    if selected_slug:
        selected_album = get_object_or_404(albums, slug=selected_slug)
    else:
        selected_album = albums.first()

    singles = Single.objects.all()

    social_links = SocialLink.objects.all()

    return render(
        request,
        "music/home.html",
        {
            "albums": albums,
            "selected_album": selected_album,
            "singles": singles,
            "social_links": social_links,
        },
    )