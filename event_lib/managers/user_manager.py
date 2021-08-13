from django.db import IntegrityError
from event_lib.managers.mysql_models import *
from event_lib.managers.cache_manager import cache_data_by_keys, set_token_by_user_id, \
    CACHE_KEY_FUNC_GET_USER_INFOS_BY_IDS
from event_lib.utils import get_timestamp
from event_lib.crypto import encrypt_token
from event_lib.constants import Result, TOKEN_EXPIRY_TIME, APP_KEY


def create_user(user_name, password_hash, user_type, salt):
    try:
        model = EventDB.UserTab.objects.create(
            user_name=user_name,
            password_hash=password_hash,
            user_type=user_type,
            salt=salt,
        )
        return model.id, None
    except IntegrityError:
        return None, Result.ERROR_ACCOUNT_EXISTED


@cache_data_by_keys(**CACHE_KEY_FUNC_GET_USER_INFOS_BY_IDS)
def get_user_infos_by_ids(user_ids):
    models = list(EventDB.UserTab.objects.filter(id__in=user_ids).values())
    return {model["id"]: model for model in models}


def is_valid_password_hash(user_id, password_hash):
    user_info = get_user_infos_by_ids([user_id]).get(user_id)
    if not user_info:
        return False
    return user_info["password_hash"] == password_hash


def get_and_set_access_token(user_id):
    token = encrypt_token(user_id, TOKEN_EXPIRY_TIME + get_timestamp(), APP_KEY).decode()
    if not set_token_by_user_id(user_id, token, TOKEN_EXPIRY_TIME):
        return None
    return token
