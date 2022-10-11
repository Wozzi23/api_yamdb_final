# Проект YaMDb


## Описание проекта

Проект YaMDb собирает отзывы пользователей  на различные  произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий может быть расширен администратором. Пользователи могут присваивать жанры путем выбора из списка заданных. Пользователи могут оставлять свои отзывы и рецензии к интересующим произведениям и выставлять свой пользовательский рейтинг (от 1 до 10). К одному произведению один пользователь может составить только одну рецензию. На основании собранных оценок происходит расчет совокупного рейтинга произведения. 
В проекте реализован REST API для моделей проекта. Аутентификация реализована с помощью JWT-токена. Также реализованы пагинация, пермишены и поиск.

-------------

## Команда проекта:
    
[Skayzer8](https://github.com/Skayzer8)
    
[Morimonster](https://github.com/Morimonster)
    
[Wozzi23](https://github.com/Wozzi23)   

-------------

## Алгоритм регистрации пользователей
    
    1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.
    2. **YaMDB** отправляет письмо с кодом подтверждения (`confirmation_code`) на адрес  `email`.
    3. Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен).
    4. При желании пользователь отправляет PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполняет поля в своём профайле (описание полей — в документации).

-------------

## Пользовательские роли
    
    - **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
    - **Аутентифицированный пользователь** (`user`) — может, как и **Аноним**, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять **свои** отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
    - **Модератор** (`moderator`) — те же права, что и у **Аутентифицированного пользователя** плюс право удалять **любые** отзывы и комментарии.
    - **Администратор** (`admin`) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям. 
    - **Суперюзер Django** — обладет правами администратора (`admin`)

-------------

## Системные требования
- Python 3.8
- Linux/Windows/MacOS

-------------

##  Технологии
    Python 3.8
    Django 2.2
    Django Rest Framework
    Simple-JWT
    PostgreSQL
    Docker
    Gunicorn
    Nginx

-------------

## Установка

1. Clone the repository to your PC:
    - git@github.com:Wozzi23/api_yamdb_final.git
2. Go to the project directory:
    - cd api_yamdb_final
3. Add .env file in the infra/ directory and describe next variables:
    
    DB_ENGINE=django.db.backends.postgresql
    
    DB_NAME= name your database
    
    POSTGRES_USER= login DB's user
    
    POSTGRES_PASSWORD= password DB's user
    
    DB_HOST=db
    
    DB_PORT=5432
    
    SECRET_KEY='django-token'
    
4. Go to the infra directory and compose image (need docker-compose):
    - cd infra
    - docker-compose up -d --build
5. After launch, in additional terminal run next commands:
    5.1. Perform migrations:
        - docker-compose exec web python manage.py migrate
    5.2. Collect static your project:
        - docker-compose exec web python manage.py collectstatic --no-input
    5.3. Create superuser your project:
        - docker-compose exec web python manage.py createsuperuser

Аfter all the steps, the project is available at:
http://127.0.0.1

Admin panel available at:
http://127.0.0.1/admin/

-------------

## Документация к проекту

Документация для API после установки доступна по адресу:

http://127.0.0.1/redoc/