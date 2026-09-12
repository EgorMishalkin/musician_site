from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ContactMessageForm
from .models import Album, Single, SiteSettings, SocialLink

def home(request):
    albums = Album.objects.prefetch_related(
        "tracks",
        "links",
        "materials",
    ).order_by("order")

    singles = Single.objects.prefetch_related("materials").all()
    social_links = SocialLink.objects.all()
    site_settings = SiteSettings.objects.first()
    selected_slug = request.GET.get("album")

    if selected_slug:
        selected_album = get_object_or_404(
            albums,
            slug=selected_slug,
        )
    else:
        cookie_slug = request.COOKIES.get("last_album")

        selected_album = (
            albums.filter(slug=cookie_slug).first()
            if cookie_slug
            else None
        )

        if selected_album is None:
            selected_album = albums.first()

    if request.method == "POST":
        contact_form = ContactMessageForm(request.POST)

        if contact_form.is_valid():
            contact_form.save()

            url = reverse("home")

            if selected_album:
                return redirect(
                    f"{url}?album={selected_album.slug}&sent=1#contact"
                )

            return redirect(f"{url}?sent=1#contact")

    else:
        contact_form = ContactMessageForm()

    response = render(
        request,
        "music/home.html",
        {
            "albums": albums,
            "selected_album": selected_album,
            "singles": singles,
            "social_links": social_links,
            "contact_form": contact_form,
            "site_settings": site_settings,
        },
    )

    if selected_album:
        response.set_cookie(
            "last_album",
            selected_album.slug,
            max_age=60 * 60 * 24 * 30,
            samesite="Lax",
        )



    return response