### praktikum_diplom


## Описание проекта
# Foodgram - «Продуктовый помощник»

Cервис где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.


## Запуск проекта с помощью Docker

1. Склонировать репозиторий на локальную машину.

    ```
    git clone 
    ```

2. Создайте .env файл в директории backend/foodgram/, в котором должны содержаться следующие переменные для подключения к базе PostgreSQL:

    ```
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    DB_HOST=db
    DB_PORT=5432
    ```

3. Перейти в директорию infra/ и выполните команду для создания и запуска контейнеров.
    ```
    sudo docker compose up -d --build
    ```


4. В контейнере backend выполнить:

    ```
    sudo docker compose exec backend python manage.py migrate
    sudo docker compose exec backend python manage.py createsuperuser
    sudo docker compose exec backend python manage.py collectstatic --no-input 
    ```

5. Загрузить в бд ингредиенты командой ниже.

    ```
    sudo docker compose exec backend python manage.py load_ingredients
    ```

6. Доступные адреса проекта:
    -  http://localhost/ - главная страница сайта;
    -  http://localhost/admin/ - админ панель;
    -  http://localhost/api/ - API проекта
    -  http://localhost/api/docs/redoc.html - документация к API

---
