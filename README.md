Полная Django-версия сайта музыкального проекта **хонисаклер**.

Проект содержит дискографию, аудиоплеер, скачивание музыки, административную панель, форму обратной связи, RU/EN локализацию и хранение данных через Django ORM.

Упрощённая статическая версия сайта используется как публичный сайт: https://honeysuckler.fun

Репозиторий: https://github.com/honeysuck1er/honeysuckler-site

Статическая версия работает без Django и базы данных и развёрнута через GitHub Pages.

## Стек

- Python 3.13
- Django 6
- SQLite
- HTML
- CSS
- JavaScript
- Django ORM
- Git

## Возможности

- отображение альбомов и синглов
- хранение дискографии в базе данных
- загрузка обложек и аудиофайлов
- встроенный аудиоплеер
- play / pause
- перемотка треков
- поддержка HTTP Range для аудио
- скачивание отдельных треков
- скачивание альбома одним ZIP-архивом
- ZIP собирается на лету без хранения второй копии MP3
- поддержка многотрековых синглов
- ссылки на музыкальные площадки
- административная панель Django
- форма обратной связи
- RU/EN локализация
- cookie для сохранения выбранного альбома
- адаптивная вёрстка

Аудиофайлы хранятся в проекте один раз и используются одновременно для воспроизведения и скачивания.

## Локальный запуск

Клонировать репозиторий:

```bash
git clone https://github.com/EgorMishalkin/musician_site.git
cd musician_site
```

Создать виртуальное окружение:

```bash
py -m venv .venv
```

Windows CMD:

```bash
.venv\Scripts\activate
```

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Установить зависимости:

```bash
pip install -r requirements.txt
```

Создать файл `.env` в корне проекта:

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

Для генерации `DJANGO_SECRET_KEY` можно использовать:

```bash
py -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Применить миграции:

```bash
py manage.py migrate
```

Загрузить данные сайта:

```bash
py manage.py loaddata defense_data.json
```

Запустить сервер:

```bash
py manage.py runserver
```

После запуска сайт доступен по адресу:

```text
http://127.0.0.1:8000/
```

## Структура аудио

```text
media/
└── audio/
    ├── albums/
    │   ├── sad-boys-club/
    │   ├── slabyy-personazh/
    │   ├── neo-emo/
    │   ├── nishtyak-muzik/
    │   ├── nishtyak-muzyka/
    │   └── piterskij-albom/
    └── singles/
```

Данные о треках и пути к аудиофайлам хранятся в базе через модели Django.

## Что реализовано на Django

В проекте используются модели:

- Album
- Track
- Single
- SingleTrack
- AlbumLink
- MaterialLink
- SocialLink
- SiteSettings
- ContactMessage

Через Django Admin можно редактировать дискографию, ссылки, треки и данные сайта.

Для аудио реализованы отдельные Django endpoints с поддержкой HTTP Range. Это позволяет браузеру нормально перематывать MP3.

При скачивании альбома Django динамически собирает ZIP из существующих аудиофайлов, поэтому отдельные ZIP-копии альбомов на диске не хранятся.

