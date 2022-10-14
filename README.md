### praktikum_diplom
[![foodgram workflow](https://github.com/mitch2424/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/mitch2424/foodgram-project-react/actions/workflows/main.yml)

Проект доступен по адресу: http://51.250.93.237/
Доступ в админку: логин admin пароль admin
# Foodgram, «Продуктовый помощник»

Cервис где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
## Уровни доступа пользователей:
- Гость (неавторизованный пользователь)
- Авторизованный пользователь
- Администратор
## Что могут делать неавторизованные пользователи
```
- Создать аккаунт.
- Просматривать рецепты на главной.
- Просматривать отдельные страницы рецептов.
- Просматривать страницы пользователей.
- Фильтровать рецепты по тегам.
```
## Что могут делать авторизованные пользователи
```
- Входить в систему под своим логином и паролем.
- Выходить из системы (разлогиниваться).
- Менять свой пароль.
- Создавать/редактировать/удалять собственные рецепты
- Просматривать рецепты на главной.
- Просматривать страницы пользователей.
- Просматривать отдельные страницы рецептов.
- Фильтровать рецепты по тегам.
- Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов.
- Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл со количеством необходимых ингредиентов для рецептов из списка покупок.
- Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок.
```
### Установка проекта :

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/mitch2424/foodgram-project-react.git
```

```
cd foodgram-project-react 
```

Cоздать и активировать виртуальное окружение:

Команда для установки виртуального окружения на Mac или Linux:
```
python3 -m venv env
source env/bin/activate
```
для Windows:
```
python -m venv venv
source venv/Scripts/activate
```

```
python -m pip install --upgrade pip
```

Установить зависимости requirements.txt:

```
cd backend
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Заполните базу тестовыми данными:
```
python manage.py loaddata dump.json
```


Создайте суперпользователя, если необходимо:
```
python manage.py createsuperuser
```

Запустить проект:

```
python manage.py runserver
```


## Установка на удалённом сервере

Необходимо добавить Action secrets в репозитории на GitHub в разделе settings -> Secrets:
* DOCKER_PASSWORD - пароль от DockerHub;
* DOCKER_USERNAME - имя пользователя на DockerHub;
* HOST - ip-адрес сервера;
* USER - пользователь для подключения;
* SSH_KEY - приватный ssh ключ (публичный должен быть на сервере);
* PASSPHRASE - если используете пароль для ssh;
* TELEGRAM_TO - id своего телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
* TELEGRAM_TOKEN - токен бота (получить токен можно у @BotFather, /token, имя бота)

В директории infra необходимо создать файл .env и заполнить его:

DB_ENGINE=django.db.backends.postgresql  # движок БД
DB_NAME=postgres  # имя БД
POSTGRES_USER=postgres  # логин для подключения к БД
POSTGRES_PASSWORD=postgres  # пароль для подключения к БД
DB_HOST=db  # название контейнера
DB_PORT=5432  # порт для подключения к БД
ALLOWED_HOSTS=*, localhost # указываем разрешенные хосты
SECRET_KEY=key # секретный ключ приложения django

### После успешного деплоя:
Соберите статику:
```
docker-compose exec backend python manage.py collectstatic --no-input
```

Примените миграции:
```
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate --noinput
```
Заполните базу тестовыми данными:
```
docker-compose exec backend python manage.py loaddata dump.json
```

Создайте суперпользователя, если необходимо:
```
docker-compose exec backend python manage.py createsuperuser
```