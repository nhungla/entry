from entry_task.views.form_schema import UserCreateUserSchema, UserPreLoginSchema, UserLoginSchema
from event_lib.managers import user_manager
from event_lib.constants import Result
from event_lib.utils import validate_params_and_process_header, api_response_data, log_info


@log_info()
@validate_params_and_process_header(form=UserCreateUserSchema, data_format="JSON")
def create_user(request, data):
    user_id, error_code = user_manager.create_user(data["user_name"], data["password_hash"], data["user_type"], data["salt"])
    if error_code:
        return api_response_data(error_code)
    return api_response_data(Result.SUCCESS, {"user_id": user_id})


@log_info()
@validate_params_and_process_header(form=UserPreLoginSchema, data_format="JSON")
def pre_login(request, data):
    user_id = data["user_id"]
    user_info = user_manager.get_user_infos_by_ids([user_id]).get(user_id)
    if not user_info:
        return api_response_data(Result.ERROR_ACCOUNT_NOT_EXISTED)
    return api_response_data(Result.SUCCESS, {"salt": user_info["salt"]})


@log_info()
@validate_params_and_process_header(form=UserLoginSchema, data_format="JSON")
def login(request, data):
    user_id = data["user_id"]
    password_hash = data["password_hash"]
    if not user_manager.is_valid_password_hash(user_id, password_hash):
        return api_response_data(Result.ERROR_LOGIN_INFO)
    access_token = user_manager.get_and_set_access_token(user_id)
    if not access_token:
        return api_response_data(Result.ERROR_SOMETHING_WRONG)
    return api_response_data(Result.SUCCESS, {"access_token": access_token})
