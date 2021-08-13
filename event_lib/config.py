import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve()

CACHE_SERVERS = {
    "redis": {
        "host": "127.0.0.1",
        "port": 6379,
    },
}


DATABASES = {
    'entry_task_db.master': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'entry_task',
        'USER': 'nhungla.phi',
        'PASSWORD': 'Asdfghjkl123456789@',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'CONN_MAX_AGE': 120,
        'OPTIONS': {'charset': 'utf8mb4'},
    },
}

DATABASES["default"] = DATABASES["entry_task_db.master"]

LOGGING_DIR = os.path.join(BASE_DIR, "../logs").replace("\\", "/")
