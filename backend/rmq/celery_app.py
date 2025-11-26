import os
from celery import Celery

#djjango настройки
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tixy_backend.settings")

broker_user = os.getenv("RABBITMQ_USERNAME", "guest")
broker_pass = os.getenv("RABBITMQ_PASSWORD", "guest")
broker_host = os.getenv("RABBITMQ_HOST", "rabbitmq.mini-helpdesk.svc.cluster.local")
broker_port = os.getenv("RABBITMQ_PORT", "5672")
broker_vhost = os.getenv("RABBITMQ_VHOST", "/")

broker_url = f"amqp://{broker_user}:{broker_pass}@{broker_host}:{broker_port}/{broker_vhost.lstrip('/')}"

result_backend = os.getenv("CELERY_RESULT_BACKEND", "rpc://")

app = Celery("tixy", broker=broker_url, backend=result_backend)

app.config_from_object("rmq.celeryconfig", namespace="CELERY")

app.autodiscover_tasks(["rmq"])
