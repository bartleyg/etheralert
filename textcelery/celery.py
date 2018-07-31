from __future__ import absolute_import, unicode_literals
from celery import Celery

import os
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'etheralert.settings')
from django.conf import settings

app = Celery('textcelery')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: etheralert.settings.INSTALLED_APPS)