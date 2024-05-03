run celery on windows:
https://celery.school/celery-on-windows

command to run celery:
celery --app=app.app worker --pool=solo

command to run flower
celery --broker=redis://localhost:6379/0 flower