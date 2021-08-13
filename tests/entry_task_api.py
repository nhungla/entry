# -*- coding: utf-8 -*-
import hashlib
import unittest
import urllib3
from test_constant import *
from event_lib.constants import Result, UserType, Channel
from event_lib.utils import get_random_string

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_access_token():
	try:
		_, result_data = request_service_api(USER_PRE_LOGIN, {"user_id": ACCOUNT_TEST["user_id"]})
		request_data = {
			"user_id": ACCOUNT_TEST["user_id"],
			"password_hash": get_password_hash(ACCOUNT_TEST["password"], result_data["salt"])
		}
		_, result_data = request_service_api(USER_LOGIN, request_data)
		return result_data["access_token"]
	except Exception as err:
		print("Error message: ", err)
		return ""


def get_password_hash(password, salt):
	combine = password + salt
	return hashlib.md5(combine.encode()).hexdigest()


access_token = get_access_token()


class AdminSmokeTest(unittest.TestCase):
	def test_create_event(self):
		request_data = {
			"start_time": "2021-05-12 00:00:00",
			"end_time": "2021-07-01 23:59:59",
			"channel": Channel.TIKTOK.value,
			"name": "Shopee-shopeeeeeeeee",
			"description": "shopeeeeeeeeee",
			"location": "HN",
			"image_url": "https://abcxyz.com",
		}
		result_code, result_data = request_service_api(ADMIN_CREATE_EVENT, request_data, access_token)
		self.assertEqual(result_code, Result.SUCCESS)


class EventSmokeTest(unittest.TestCase):
	def test_get_ids_and_infos(self):
		request_data = {
			"start_time": "2021-06-12 00:00:00",
			"end_time": "2021-07-01 23:59:59",
			"channels": [Channel.FACEBOOK.value, Channel.TIKTOK.value]
		}
		result_code, result_data = request_service_api(EVENT_GET_IDS, request_data, access_token)
		self.assertEqual(result_code, Result.SUCCESS)

		result_code, result_data = request_service_api(EVENT_GET_INFOS_BY_IDS, {"event_ids": result_data["event_ids"]}, access_token)
		self.assertEqual(result_code, Result.SUCCESS)

	def test_get_detail(self):
		request_data = {
			"event_id": 1
		}
		result_code, result_data = request_service_api(EVENT_GET_DETAIL, request_data, access_token)
		self.assertEqual(result_code, Result.SUCCESS)

	def test_comment(self):
		request_data = {
			"event_id": 1,
			"comment": "shopee shopee shopee shopee shopee..."
		}
		result_code, result_data = request_service_api(EVENT_COMMENT, request_data, access_token)
		self.assertEqual(result_code, Result.SUCCESS)

	def test_like(self):
		request_data = {
			"event_id": 1,
		}
		result_code, result_data = request_service_api(EVENT_LIKE, request_data, access_token)
		self.assertEqual(result_code, Result.SUCCESS)

	def test_participate(self):
		request_data = {
			"event_id": 1,
			"comment": "shopee shopee shopee shopee shopee..."
		}
		result_code, result_data = request_service_api(EVENT_COMMENT, request_data, access_token)
		self.assertEqual(result_code, Result.SUCCESS)


class UserSmokeTest(unittest.TestCase):
	def setUp(self) -> None:
		self.password = "12345678910"
		self.user_id = 2

	def test_create(self):
		salt = get_random_string(20)
		user_type = UserType.ADMIN.value
		request_data = {
			"user_name": "nhunglp.%s" % get_random_string(10),
			"password_hash": get_password_hash(self.password, salt),
			"salt": salt,
			"user_type": user_type
		}
		result_code, result_data = request_service_api(USER_CREATE_USER, request_data, access_token)
		self.assertEqual(result_code, Result.SUCCESS)

	def test_login(self):
		request_data = {
			"user_id": self.user_id,
		}
		result_code, result_data = request_service_api(USER_PRE_LOGIN, request_data, access_token)
		self.assertEqual(result_code, Result.SUCCESS)

		request_data = {
			"user_id": self.user_id,
			"password_hash": get_password_hash(self.password, result_data["salt"])
		}
		result_code, result_data = request_service_api(USER_LOGIN, request_data, access_token)
		self.assertEqual(result_code, Result.SUCCESS)


if __name__ == "__main__":
	unittest.main()
