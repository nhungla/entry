import os
import sys
import json
import requests


os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append('../')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ACCOUNT_TEST = {
	"user_id": 2,
	"password": "12345678910"
}


ENTRY_TASK_URL = "http://127.0.0.1:8000/api"

ADMIN_CREATE_EVENT = ENTRY_TASK_URL + "/admin/create_event"

EVENT_COMMENT = ENTRY_TASK_URL + "/event/comment"
EVENT_LIKE = ENTRY_TASK_URL + "/event/like"
EVENT_PARTICIPATE = ENTRY_TASK_URL + "/event/participate"
EVENT_GET_DETAIL = ENTRY_TASK_URL + "/event/get_detail"
EVENT_GET_IDS = ENTRY_TASK_URL + "/event/get_ids"
EVENT_GET_INFOS_BY_IDS = ENTRY_TASK_URL + "/event/get_infos_by_ids"

USER_CREATE_USER = ENTRY_TASK_URL + "/user/create_user"
USER_PRE_LOGIN = ENTRY_TASK_URL + "/user/pre_login"
USER_LOGIN = ENTRY_TASK_URL + "/user/login"


def request_service_api(url, data, access_token="", method="POST"):
	headers = {
		'X-Entry-Task-Access-Token': access_token,
	}
	if method == "POST":
		response = requests.post(url, data=json.dumps(data), verify=False, headers=headers)
	else:
		response = requests.get(url, params=data, verify=False, headers=headers)
	try:
		if response.status_code != 200:
			print("REQUEST HTTP ERROR CODE: %s" % response.status_code)
			return None, None
		result = response.json()
		result_code = result["result"]
		result_body = result.get("reply")
		return result_code, result_body
	except Exception as error:
		print("  REQUEST EXCEPTION: %s" % error)
	return None, None
