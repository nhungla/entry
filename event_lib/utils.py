import datetime
import json
import logging
import time
import random
import jsonschema
import string
from django import http
from functools import wraps
from event_lib.constants import Result, DATETIME_FORMAT

logger = logging.getLogger("print_info")
logger.setLevel(logging.DEBUG)


def timestamp_to_string(timestamp, format=DATETIME_FORMAT):
    dt = datetime.datetime.fromtimestamp(int(timestamp))
    return dt.strftime(format)


def get_timestamp():
    return int(time.time())


def from_json(s):
    return json.loads(s)


def to_json(data, ensure_ascii=False, default=None):
    return json.dumps(data, ensure_ascii=ensure_ascii, separators=(',', ':'), default=default)


def api_response(request, data):
    response = http.HttpResponse(to_json(data), content_type='application/json; charset=utf-8')
    return response


def normalize_data(value):
    return str(value)


def api_response_data(result_code, reply=None):
    response = http.HttpResponse(
        to_json({"result": result_code, "reply": reply}, ensure_ascii=False, default=normalize_data)
    )
    response['content-type'] = 'application/json; charset=utf-8'
    return response


def _validate_params(request, form, data_format):
    if data_format == "JSON":
        try:
            jsonschema.validate(instance=request, schema=form)
        except:
            return Result.ERROR_PARAMS
    else:
        raise Exception("Not implemented")


def validate_params_and_process_header(form, data_format="JSON"):
    def _validate_param(func):
        @wraps(func)
        def _func(request, *args, **kwargs):
            header = request.META
            data = {}
            if header.get("HTTP_X_ENTRY_TASK_ACCESS_TOKEN"):
                data["access_token"] = header["HTTP_X_ENTRY_TASK_ACCESS_TOKEN"]
            data.update(from_json(request.body))
            error_code = _validate_params(data, form, data_format)
            if error_code:
                return api_response_data(error_code)
            return func(request, data, *args, **kwargs)
        return _func
    return _validate_param


def get_random_string(length=20):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def parse_string_to_date(str_date, dt_format=DATETIME_FORMAT):
    if not str_date:
        return None
    str_date = str_date.strip()
    date_result = None
    try:
        date_result = datetime.datetime.strptime(str_date, dt_format)
    except Exception as ex:
        pass
    return date_result


def naive_datetime_to_timestamp(dt):
    if dt is None:
        return None
    return int(time.mktime(dt.timetuple()))


def parse_string_to_timestamp(str_date, dt_format=DATETIME_FORMAT):
    parse_date = parse_string_to_date(str_date, dt_format)
    return naive_datetime_to_timestamp(parse_date) if parse_date else 0


def log_info():
    def _log_info(func):
        @wraps(func)
        def _func(request, *args, **kwargs):
            start_time = time.time()
            try:
                response = func(request, *args, **kwargs)
            except Exception as err:
                logger.exception("method=%s,url=%s,error=%s" % (request.method, request.get_full_path().encode('utf-8'), err))
                raise
            elapsed_time = time.time() - start_time
            logger.info("elapsed_time=%s,method=%s,url=%s" % (elapsed_time, request.method, request.get_full_path().encode('utf-8')))
            return response
        return _func
    return _log_info
