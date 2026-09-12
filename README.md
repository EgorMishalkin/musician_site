# хонисаклер — Django musician website

Учебный проект по дисциплине «Технологии web-программирования».

Сайт музыканта, разработанный на Python и Django.

## Возможности

- дискография и треклисты;
- выбор альбома через GET-параметр;
- русский и английский интерфейс;
- пользовательская cookie `last_album`;
- POST-форма обратной связи;
- Django Admin;
- дополнительные ссылки и материалы для релизов;
- адаптивная версия сайта;
- unit-тесты.

## Требования

- Python 3.13
- pip
- Windows 10/11
- PowerShell

## Запуск проекта

Скачать ZIP ветки `localhost-branch`, распаковать архив и открыть PowerShell в папке проекта.

### 1. Создать виртуальное окружение

```powershell
py -3.13 -m venv .venv
```

### 2. Разрешить запуск скриптов в текущем окне PowerShell

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Настройка действует только до закрытия текущего окна PowerShell.

### 3. Активировать виртуальное окружение

```powershell
.\.venv\Scripts\Activate.ps1
```

После активации в начале строки должно появиться:

```text
(.venv)
```

### 4. Установить зависимости

```powershell
python -m pip install -r requirements.txt
```

### 5. Создать локальный файл настроек

```powershell
Copy-Item .env.example .env
```

### 6. Выполнить миграции

```powershell
python manage.py migrate
```

### 7. Загрузить демонстрационные данные

```powershell
python manage.py loaddata defense_data.json
```

### 8. Запустить unit-тесты

```powershell
python manage.py test
```

Ожидаемый результат:

```text
Ran 4 tests
OK
```

### 9. Запустить сервер

```powershell
python manage.py runserver
```

После запуска сайт доступен по адресу:

http://127.0.0.1:8000/

Важно: локальный Django-сервер запускается по HTTP, а не HTTPS.

В проекте реализованы тесты:

- выбора альбома через GET-параметр;
- восстановления выбранного альбома через cookie;
- отправки POST-формы обратной связи;
- обработки запроса к несуществующему релизу.

## Структура проекта

```text
musician_site/
├── config/                 настройки Django
├── locale/                 файлы локализации
├── media/                  обложки и изображения
├── music/                  основное Django-приложение
├── defense_data.json       демонстрационные данные
├── .env.example            пример локальных настроек
├── manage.py
├── requirements.txt
└── README.md
```

## Используемые технологии

- Python
- Django
- HTML
- CSS
- SQLite
- Django ORM
- Django Templates
- Django i18n
- Git
