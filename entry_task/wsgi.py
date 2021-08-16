"""
WSGI config for entry_task project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import platform
import logging
import pathlib
from gevent import monkey
from event_lib import config
from event_lib.constants import DATETIME_FORMAT

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'entry_task.settings')

application = get_wsgi_application()

if "window" not in platform.system().lower():
    file_path = os.path.join(config.LOGGING_DIR, "info.txt")
    try:
        os.mkdir(config.LOGGING_DIR)
        pathlib.Path(file_path).touch(mode=777)
    except:
        pass
    logging.basicConfig(filename=file_path, filemode='a', format='%(message)s', datefmt=DATETIME_FORMAT)
    monkey.patch_all()
