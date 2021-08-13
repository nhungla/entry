"""
WSGI config for entry_task project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import platform
import pathlib
import logging
from gevent import monkey
from event_lib import config

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'entry_task.settings')

application = get_wsgi_application()

if "window" not in platform.system().lower():
    monkey.patch_all()
    file_path = os.path.join(config.LOGGING_DIR, "info.txt")
    try:
        os.mkdir(config.LOGGING_DIR)
        pathlib.Path(file_path).touch(mode=777)
    except:
        pass
    logging.basicConfig(filename=config.LOGGING_DIR, filemode='a', format='%(name)s - %(levelname)s - %(message)s')

#logging.info()
#logging.exception()
#logging.error()
#logging.debug()
