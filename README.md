# MyProject

Проект Django для работы с пользовательской моделью и базой данных Microsoft SQL Server.

---

## Описание проекта

Этот проект представляет собой веб-приложение на основе фреймворка Django. Он использует пользовательскую модель `CustomUser` для управления пользователями и подключается к базе данных Microsoft SQL Server через драйвер ODBC.

Основные функции:
- Админка Django для управления пользователями.
- Пользовательская модель `CustomUser` с дополнительными полями (например, номер телефона, адрес, дата рождения).
- Поддержка базы данных Microsoft SQL Server.

---

## Требования

Для работы с проектом вам потребуется:
- Python 3.12+
- Django 4.2
- База данных: Microsoft SQL Server
- Драйвер: ODBC Driver 17 for SQL Server
- Виртуальное окружение Python (рекомендуется)

---

## Установка

### 1. Клонирование репозитория
Склонируйте репозиторий на ваш компьютер:
```bash
git clone - еще не сделал
cd myproject

Создайте и активируйте виртуальное окружение: python -m venv .venv
.venv\Scripts\activate

Установите зависимости из файла requirements.txt: pip install -r requirements.txt

Создайте файл .env в корне проекта и добавьте следующие переменные: 

DB_NAME=dogs
DB_USER=sa
DB_PASSWORD=your_password
DB_HOST=localhost\SQLEXPRESS
DB_PORT=1433
SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

Примените миграции для создания таблиц в базе данных: python manage.py migrate

Создайте суперпользователя для доступа к админке Django: python manage.py createsuperuser

Запустите сервер разработки Django: python manage.py runserver