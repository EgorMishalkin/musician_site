# Хонисаклер — Django musician website

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

Скачать ZIP ветки `lab-defense`, распаковать архив и открыть PowerShell в папке проекта.

### 1. Создать виртуальное окружение

```powershell
python -m venv .venv
```

### 2. Активировать виртуальное окружение

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Установить зависимости

```powershell
python -m pip install -r requirements.txt
```

### 4. Создать локальный файл настроек

```powershell
Copy-Item .env.example .env
```

### 5. Выполнить миграции

```powershell
python manage.py migrate
```

### 6. Загрузить демонстрационные данные

```powershell
python manage.py loaddata defense_data.json
```

### 7. Запустить сервер

```powershell
python manage.py runserver
```

После запуска сайт доступен по адресу:

http://127.0.0.1:8000/

## Django Admin

Чтобы использовать административную панель, необходимо создать суперпользователя:

```powershell
python manage.py createsuperuser
```

После этого запустить сервер:

```powershell
python manage.py runserver
```

Административная панель доступна по адресу:

http://127.0.0.1:8000/admin/

## Unit-тесты

Для запуска тестов:

```powershell
python manage.py test
```

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