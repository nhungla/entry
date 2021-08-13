import multiprocessing
import sys
import os

sys.path.append('./')

app_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

worker_class = "gevent"
worker_connections = 50
timeout = 1200
graceful_timeout = 60
daemon = False
workers = multiprocessing.cpu_count() * 2
bind = "127.0.0.1:8000"
