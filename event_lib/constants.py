from enum import Enum
MIN_ARRAY_SIZE = 1
MAX_ARRAY_SIZE = 100
TYPE_UINT8_MAX = 255
TYPE_UINT64_MAX = 18446744073709551615
APP_KEY = b'7-gIcNBHqqjB3Y1CBzUheiZMSHObIQgvioTtk_Qqg04='
TOKEN_EXPIRY_TIME = 60 * 60
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"
DATETIME_FORMAT = DATE_FORMAT + " " + TIME_FORMAT


class EnumBase(Enum):
    @classmethod
    def get_max(cls):
        return max(c.value for c in cls)

    @classmethod
    def get_min(cls):
        return min(c.value for c in cls)


class Result:
    ERROR_ACCESS_TOKEN = "error_access_token"
    ERROR_ACCOUNT_EXISTED = "error_account_existed"
    ERROR_ACCOUNT_NOT_EXISTED = "error_account_not_existed"
    ERROR_INVALID_TIME_RANGE = "error_invalid_time_range"
    ERROR_INVALID_PERMISSION = "error_invalid_permission"
    ERROR_LOGIN_INFO = "error_login_info"
    ERROR_PARAMS = "error_params"
    ERROR_SOMETHING_WRONG = "error_something_wrong"
    SUCCESS = "success"


class Channel(EnumBase):
    FACEBOOK = 1
    INSTAGRAM = 2
    TIKTOK = 3


class UserType(EnumBase):
    NORMAL = 1
    ADMIN = 2
