# Построение рекомендательной системы для продвижения партнерских услуг физическим лицам коммерческого банка на основе данных их транзакций

Данный проект является макетом сервиса, цель которого обеспечить методы взаимодействия клиентов и сотрудников с рекомендательной системой.

Демо сервиса доступно по http://81.88.118.62/

### Installing

Проект использует:
- django - https://www.djangoproject.com,
- django REST framework - https://www.django-rest-framework.org,
- PostgreSQL - https://www.postgresql.org,
- celery - https://docs.celeryproject.org/en/stable/index.html,
- redis - https://redis.io,
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
    
Запустить redis:

    'docker-compose up'

Запустить сервер:
    
    'python manage.py runserver'

Запустить celery:

    'celery -A recsystem beat'
    'celery -A recsystem worker -l INFO --pool=solo'
    
### Authors

[knyht](https://github.com/knyht) - Разработка модели рекомендатлньой системы на машинном обучение.

[AleksandrRadist](https://github.com/AleksandrRadist) - Проектирование и разработка сайта и API.
