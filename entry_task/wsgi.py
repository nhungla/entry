"""
WSGI config for entry_task project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import platform
from gevent import monkey

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'entry_task.settings')

application = get_wsgi_application()

if "window" not in platform.system().lower():
    print("monkey patch for application")
    monkey.patch_all()
