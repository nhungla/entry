import sys
import os
import django
import time

curr_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(curr_dir)
sys.path.append(os.path.join(curr_dir, '../'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "entry_task.settings")
django.setup()

import random
import hashlib
from event_lib.managers.mysql_models import *
import event_lib.utils as ut


def get_password_hash(password, salt):
    combine = password + salt
    return hashlib.md5(combine.encode()).hexdigest()


if __name__ == "__main__":
    print("Start to fill data")
    start_time = ut.get_timestamp()
    password = "12345678910"
    for i in range(100, 100 + 1001):
        salt = ut.get_random_string(20)
        EventDB.UserTab.objects.create(
            user_name="nhunglp.%s" % i,
            password_hash=get_password_hash(password, salt),
            salt=salt,
            user_type=random.randint(1, 2)
        )
    time.sleep(0.1)
    print("End to fill data!")
