import mimetypes
import re
import tempfile
import zipfile
from pathlib import Path

from django.http import (
    FileResponse,
    Http404,
    HttpResponse,
    StreamingHttpResponse,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ContactMessageForm
from .models import (
    Album,
    Single,
    SingleTrack,
    SiteSettings,
    SocialLink,
    Track,
)


def home(request):
    albums = Album.objects.prefetch_related(
        "tracks",
        "links",
        "materials",
    ).order_by("order")

    singles = Single.objects.prefetch_related(
        "materials",
        "tracks",
    ).all()

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
                    f"{url}?album={selected_album.slug}"
                    "&sent=1#contact"
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


def _safe_filename(value):
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", value)
    value = value.strip().rstrip(".")
    return value or "file"


def _range_chunks(file_obj, length, chunk_size=64 * 1024):
    remaining = length

    try:
        while remaining > 0:
            chunk = file_obj.read(min(chunk_size, remaining))
            if not chunk:
                break

            remaining -= len(chunk)
            yield chunk
    finally:
        file_obj.close()


def _stream_audio(request, field_file):
    if not field_file:
        raise Http404("Аудиофайл не загружен.")

    path = Path(field_file.path)

    if not path.exists():
        raise Http404("Аудиофайл не найден.")

    size = path.stat().st_size
    content_type = (
        mimetypes.guess_type(path.name)[0]
        or "audio/mpeg"
    )
    range_header = request.headers.get("Range")

    if not range_header:
        response = FileResponse(
            path.open("rb"),
            content_type=content_type,
        )
        response["Content-Length"] = str(size)
        response["Accept-Ranges"] = "bytes"
        return response

    match = re.fullmatch(
        r"bytes=(\d*)-(\d*)",
        range_header.strip(),
    )

    if not match:
        response = HttpResponse(status=416)
        response["Content-Range"] = f"bytes */{size}"
        return response

    start_text, end_text = match.groups()

    try:
        if start_text:
            start = int(start_text)
            end = (
                int(end_text)
                if end_text
                else size - 1
            )
        else:
            suffix_length = int(end_text)
            if suffix_length <= 0:
                raise ValueError

            start = max(size - suffix_length, 0)
            end = size - 1
    except ValueError:
        response = HttpResponse(status=416)
        response["Content-Range"] = f"bytes */{size}"
        return response

    if (
        start < 0
        or start >= size
        or end < start
    ):
        response = HttpResponse(status=416)
        response["Content-Range"] = f"bytes */{size}"
        return response

    end = min(end, size - 1)
    length = end - start + 1

    file_obj = path.open("rb")
    file_obj.seek(start)

    response = StreamingHttpResponse(
        _range_chunks(file_obj, length),
        status=206,
        content_type=content_type,
    )
    response["Content-Length"] = str(length)
    response["Content-Range"] = (
        f"bytes {start}-{end}/{size}"
    )
    response["Accept-Ranges"] = "bytes"
    return response


def stream_album_track(request, pk):
    track = get_object_or_404(Track, pk=pk)
    return _stream_audio(request, track.audio)


def stream_single_track(request, pk):
    track = get_object_or_404(SingleTrack, pk=pk)
    return _stream_audio(request, track.audio)


def _download_audio(field_file, title):
    if not field_file:
        raise Http404("Аудиофайл не загружен.")

    path = Path(field_file.path)

    if not path.exists():
        raise Http404("Аудиофайл не найден.")

    suffix = path.suffix or ".mp3"

    return FileResponse(
        path.open("rb"),
        as_attachment=True,
        filename=f"{_safe_filename(title)}{suffix}",
        content_type=(
            mimetypes.guess_type(path.name)[0]
            or "application/octet-stream"
        ),
    )


def download_album_track(request, pk):
    track = get_object_or_404(Track, pk=pk)
    return _download_audio(track.audio, track.title)


def download_single_track(request, pk):
    track = get_object_or_404(SingleTrack, pk=pk)
    return _download_audio(track.audio, track.title)


def download_album(request, slug):
    album = get_object_or_404(
        Album.objects.prefetch_related("tracks"),
        slug=slug,
    )

    tracks = [
        track
        for track in album.tracks.all()
        if track.audio
        and Path(track.audio.path).exists()
    ]

    if not tracks:
        raise Http404("У альбома нет загруженных треков.")

    archive_file = tempfile.SpooledTemporaryFile(
        max_size=16 * 1024 * 1024,
        mode="w+b",
    )

    with zipfile.ZipFile(
        archive_file,
        mode="w",
        compression=zipfile.ZIP_STORED,
    ) as archive:
        for track in tracks:
            source = Path(track.audio.path)
            archive_name = (
                f"{track.number:02d} - "
                f"{_safe_filename(track.title)}"
                f"{source.suffix or '.mp3'}"
            )
            archive.write(
                source,
                arcname=archive_name,
            )

    archive_file.seek(0)

    return FileResponse(
        archive_file,
        as_attachment=True,
        filename=f"{_safe_filename(album.title)}.zip",
        content_type="application/zip",
    )
