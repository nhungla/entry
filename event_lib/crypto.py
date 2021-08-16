import time
from cryptography.fernet import Fernet

TOKEN_FORMAT = "%s,%s,%s"  # user_id, expiry_time, create_time


def encrypt_token(user_id, expiry_time, key):
    message = TOKEN_FORMAT % (user_id, expiry_time, int(time.time()))
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())


def decrypt_token(token, key):
    fernet = Fernet(key)
    try:
        data = fernet.decrypt(token.encode()).decode()
        return list(map(int, data.split(",")))
    except:
        return None
