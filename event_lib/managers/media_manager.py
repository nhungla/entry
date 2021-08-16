import base64
import os
from entry_task.settings import STATIC_URL
from event_lib.utils import logger, timestamp_to_string, get_timestamp, get_random_string
from event_lib.constants import DATE_FORMAT
from event_lib import config


def save_image(image_base_64_content, extension):
    cur_timestamp = get_timestamp()
    cur_date_str = timestamp_to_string(cur_timestamp, DATE_FORMAT)
    try:
        new_file_name = "%s_%s.%s" % (get_random_string(10), cur_timestamp, extension)
        file_content = base64.b64decode(image_base_64_content)
        folder_path = os.path.join(STATIC_URL, cur_date_str)
        try:
            os.mkdir(folder_path)
        except:
            pass
        image_file_path = os.path.join(folder_path, new_file_name)
        with open(image_file_path, "wb+") as f:
            f.write(file_content)
        return "%s/%s/%s" % (config.DOMAIN_NAME, cur_date_str, new_file_name)
    except Exception as err:
        logger.exception("save_image_failed|error=%s" % err)
        return ""
