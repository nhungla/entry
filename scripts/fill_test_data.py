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
from event_lib.managers.mysql_models import *
import event_lib.utils as ut
from event_lib.constants import Channel


if __name__ == "__main__":
	"""
	for _ in range(1000000):
		EventDB.EventTab.objects.create(
			create_uid=random.randint(2, 15),
			create_time=ut.get_timestamp(),
			start_time=ut.get_timestamp() + random.randint(60 * 60, 60 * 60 * 30),
			end_time=ut.get_timestamp() + random.randint(60 * 60 * 10, 60 * 60 * 150),
			channel=random.randint(Channel.get_min(), Channel.get_max()),
			extra_data=ut.to_json(
				{
					"location": "Ho Chi Minh City",
					"name": "Birthday",
					"image_url": "http://192.168.1.182/static/2021-08-13/SDUMW674BS_1628849525.jpg",
					"description": "9/9",
				}
			)
		)
"""
	print("Start to fill data")
	start_time = ut.get_timestamp()
	for _ in range(10000):
		models = []
		start_time += 24 * 60 * 60
		for _ in range(100):
			models.append(EventDB.EventTab(
				create_uid=random.randint(2, 15),
				create_time=ut.get_timestamp(),
				start_time=start_time,
				end_time=start_time + 24 * 60 * 60,
				channel=random.randint(Channel.get_min(), Channel.get_max()),
				extra_data=ut.to_json(
					{
						"location": "Ho Chi Minh City",
						"name": "Birthday",
						"image_url": "http://192.168.1.182/static/2021-08-13/SDUMW674BS_1628849525.jpg",
						"description": "9/9",
					}
				)
			))
		EventDB.EventTab.objects.bulk_create(models)
		time.sleep(0.1)

	print("End to fill data!")
