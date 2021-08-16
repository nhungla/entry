from event_lib.crypto import decrypt_token
from event_lib.constants import Result, APP_KEY, UserType
from event_lib.utils import api_response_data
from event_lib.managers import cache_manager, user_manager


def verify_access_token(is_required_admin=False):
    def _verify_access_token(func):
        def _func(request, data, *args, **kwargs):
            if not data.get("access_token"):
                return api_response_data(Result.ERROR_ACCESS_TOKEN)
            session_infos = decrypt_token(data["access_token"], APP_KEY)
            if not session_infos:
                return api_response_data(Result.ERROR_ACCESS_TOKEN)
            user_id = session_infos[0]
            redis_token = cache_manager.get_token_by_user_id(user_id)
            if redis_token != data["access_token"]:
                return api_response_data(Result.ERROR_ACCESS_TOKEN)
            if is_required_admin:
                user_info = user_manager.get_user_infos_by_ids([user_id]).get(user_id)
                if not user_info or user_info["user_type"] != UserType.ADMIN.value:
                    return api_response_data(Result.ERROR_INVALID_PERMISSION)
            data["user_id"] = user_id
            return func(request, data, *args, **kwargs)
        return _func
    return _verify_access_token
