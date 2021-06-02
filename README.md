# Recommendation System

Построение рекомендательной системы для продвижения партнерских услуг физическим лицам коммерческого банка на основе данных их транзакций

Данный проект является макетом сервиса, цель которого обеспечить методы взаимодействия клиентов и сотрудников с рекомендательной системой.

### Installing

Проект использует:
- django - https://www.djangoproject.com,
- django REST framework - https://www.django-rest-framework.org,
- PostgreSQL - https://www.postgresql.org,
- nginx - https://nginx.org/ru/.

### Чтобы запустить проект необходимо:

Создать и активировать виртуальное окружение:

    'python -m venv venv'
    'venv\Scripts\activate'

Установить зависимости: 

    'pip install -r requirements.txt'
    
Запустить миграции: 

    'python manage.py migrate
    
Загрузить тестовые данные:

    'python manage.py loaddata data2.json'

Cоздать суперпользователя:

    'python manage.py createsuperuser'

Запустить сервер:
    
    'python manage.py runserver'

### Authors

[knyht](https://github.com/knyht) - разработка модели рекомендатлньой системы на машинном обучение.

[AleksandrRadist](https://github.com/AleksandrRadist) - Проектирование и разработка сайта и API.

