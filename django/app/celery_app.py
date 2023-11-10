import os

from celery import Celery
from kombu.transport.redis import GlobalKeyPrefixMixin

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

if "WATCH" not in GlobalKeyPrefixMixin.PREFIXED_COMPLEX_COMMANDS:
    # Remove when fixed https://github.com/celery/kombu/issues/1569
    GlobalKeyPrefixMixin.PREFIXED_COMPLEX_COMMANDS["WATCH"] = {
        "args_start": 0,
        "args_end": None,
    }

celery_app = Celery("app")

celery_app.config_from_object("django.conf:settings", namespace="CELERY")

celery_app.autodiscover_tasks()
