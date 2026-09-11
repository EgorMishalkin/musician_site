import sys
from urllib.parse import quote, quote_plus

import requests


ARTIST_NAME = "хонисаклер"

# 5 секунд на подключение, 20 секунд на получение ответа
TIMEOUT = (5, 20)

HEADERS = {
    "User-Agent": "musician_site/0.1"
}


def normalize(value):
    return value.strip().casefold()


def is_correct_release(album_title, artist_name, wanted_title):
    return (
        normalize(album_title) == normalize(wanted_title)
        and normalize(artist_name) == normalize(ARTIST_NAME)
    )


def search_deezer(title):
    response = requests.get(
        "https://api.deezer.com/search/album",
        params={
            "q": f'artist:"{ARTIST_NAME}" album:"{title}"',
            "limit": 25,
        },
        headers=HEADERS,
        timeout=TIMEOUT,
    )

    response.raise_for_status()

    albums = response.json().get("data", [])

    for album in albums:
        artist = album.get("artist", {}).get("name", "")

        if not is_correct_release(
            album.get("title", ""),
            artist,
            title,
        ):
            continue

        album_id = album["id"]

        details = requests.get(
            f"https://api.deezer.com/album/{album_id}",
            headers=HEADERS,
            timeout=TIMEOUT,
        )

        details.raise_for_status()

        return details.json()

    return None


def search_deezer_by_upc(upc):
    response = requests.get(
        f"https://api.deezer.com/album/upc:{upc}",
        headers=HEADERS,
        timeout=TIMEOUT,
    )

    response.raise_for_status()

    data = response.json()

    if "error" in data:
        return None

    return data


def search_apple_music(title):
    for country in ("ru", "us"):
        response = requests.get(
            "https://itunes.apple.com/search",
            params={
                "term": f"{ARTIST_NAME} {title}",
                "country": country,
                "media": "music",
                "entity": "album",
                "limit": 25,
            },
            headers=HEADERS,
            timeout=TIMEOUT,
        )

        response.raise_for_status()

        results = response.json().get("results", [])

        for album in results:
            if is_correct_release(
                album.get("collectionName", ""),
                album.get("artistName", ""),
                title,
            ):
                return album.get("collectionViewUrl")

    return None


def search_yandex_music(title):
    response = requests.get(
        "https://api.music.yandex.net/search",
        params={
            "text": f"{ARTIST_NAME} {title}",
            "type": "album",
            "page": 0,
            "nocorrect": "true",
        },
        headers=HEADERS,
        timeout=TIMEOUT,
    )

    response.raise_for_status()

    albums = (
        response.json()
        .get("result", {})
        .get("albums", {})
        .get("results", [])
    )

    for album in albums:
        artists = album.get("artists", [])

        artist_names = [
            artist.get("name", "")
            for artist in artists
        ]

        correct_artist = any(
            normalize(name) == normalize(ARTIST_NAME)
            for name in artist_names
        )

        correct_title = (
            normalize(album.get("title", ""))
            == normalize(title)
        )

        if correct_title and correct_artist:
            return f"https://music.yandex.ru/album/{album['id']}"

    return None


def safe_lookup(func, *args):
    try:
        return func(*args)

    except requests.RequestException as error:
        print(
            f"Ошибка при обращении к {func.__name__}: "
            f"{error}"
        )

        return None


def lookup_release(title):
    """
    Ищет релиз по названию.

    Возвращает словарь:
    {
        "title": "...",
        "upc": "...",
        "links": {
            "Deezer": "...",
            "Apple Music": "...",
            "Yandex Music": "...",
        }
    }
    """

    deezer_album = safe_lookup(
        search_deezer,
        title,
    )

    upc = (
        deezer_album.get("upc")
        if deezer_album
        else None
    )

    links = {
        "Deezer": (
            deezer_album.get("link")
            if deezer_album
            else None
        ),

        "Apple Music": safe_lookup(
            search_apple_music,
            title,
        ),

        "Yandex Music": safe_lookup(
            search_yandex_music,
            title,
        ),
    }

    return {
        "title": title,
        "upc": upc,
        "links": links,
    }


def fallback_links(title):
    """
    Если прямую ссылку получить не удалось,
    можем хотя бы сформировать ссылки на поиск.
    """

    query = f"{ARTIST_NAME} {title}"

    return {
        "Spotify search":
            "https://open.spotify.com/search/"
            + quote(query, safe=""),

        "YouTube Music search":
            "https://music.youtube.com/search?q="
            + quote_plus(query),

        "SoundCloud search":
            "https://soundcloud.com/search?q="
            + quote_plus(query),
    }


def print_result(title, upc, links):
    print()
    print("=" * 60)
    print(f"Артист: {ARTIST_NAME}")
    print(f"Релиз:  {title}")
    print(f"UPC:    {upc or 'не найден'}")
    print("=" * 60)

    for service, url in links.items():
        if url:
            print(f"{service}:")
            print(url)
        else:
            print(f"{service}: не найден")

        print()


def lookup_by_upc(upc):
    deezer_album = safe_lookup(
        search_deezer_by_upc,
        upc,
    )

    if not deezer_album:
        return None

    title = deezer_album.get("title")

    links = {
        "Deezer": deezer_album.get("link"),

        "Apple Music": safe_lookup(
            search_apple_music,
            title,
        ),

        "Yandex Music": safe_lookup(
            search_yandex_music,
            title,
        ),
    }

    return {
        "title": title,
        "upc": upc,
        "links": links,
    }


def main():
    if len(sys.argv) < 2:
        print(
            'Пример:\n'
            'python -m music.services.release_lookup '
            '"neo emo"'
        )
        return

    value = " ".join(sys.argv[1:]).strip()

    if value.isdigit():
        result = lookup_by_upc(value)

        if not result:
            print("Релиз с таким UPC не найден.")
            return

    else:
        result = lookup_release(value)

    links = result["links"]

    # Только для вывода в терминал.
    # В базу эти поисковые ссылки не сохраняем.
    links.update(
        fallback_links(result["title"])
    )

    print_result(
        result["title"],
        result["upc"],
        links,
    )


if __name__ == "__main__":
    main()