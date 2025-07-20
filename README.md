# fixplus Project

## project setup

1- compelete cookiecutter workflow (recommendation: leave project_slug empty) and go inside the project
```
cd fixplus-back
```

2- Setup venv
```
virtualenv -p python3.11 venv
source venv/bin/activate
```

3- install Dependencies
```
pip install -r requirements/dev.txt
```

4- create your env
```
cp .env.example .env
```

5- spin off docker compose
```
docker compose -f docker-compose.dev.yml up -d
```

6- Create tables
```
python manage.py migrate
```

7- run the project
```
python manage.py runserver 0.0.0.0:8000
```

8- run Celery
```
celery -A src.tasks worker --loglevel=info -P eventlet
celery -A src.tasks worker -l info --without-gossip --without-mingle --without-heartbeat
```

9- run Beats
```
python manage.py setup_periodic_tasks
celery -A src.tasks beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

9- create and compile translate
```
django-admin makemessages -l fa --ignore 'venv/*'
django-admin compilemessages
```