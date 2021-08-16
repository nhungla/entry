from entry_task.views.form_schema import EventGetInfosByIdsSchema, EventGetIdsSchema, \
    EventGetDetailSchema, EventCommentSchema, EventLikeSchema, EventParticipateSchema, EventGetIdsSchemaV2
from event_lib.managers import event_manager
from event_lib.constants import Result
from event_lib.verify_access_token import verify_access_token
from event_lib.utils import validate_params_and_process_header, api_response_data, \
    parse_string_to_timestamp, log_info

MAX_TIME_RANGE = 30 * 24 * 60 * 60


@log_info()
@validate_params_and_process_header(form=EventCommentSchema, data_format="JSON")
@verify_access_token()
def comment(request, data):
    event_manager.comment_on_event(data["user_id"], data["event_id"], data["comment"])
    return api_response_data(Result.SUCCESS)


@log_info()
@validate_params_and_process_header(form=EventLikeSchema, data_format="JSON")
@verify_access_token()
def like(request, data):
    event_manager.like_event(data["user_id"], data["event_id"])
    return api_response_data(Result.SUCCESS)


@log_info()
@validate_params_and_process_header(form=EventGetDetailSchema, data_format="JSON")
@verify_access_token()
def get_detail(request, data):
    detail = event_manager.get_detail(data["event_id"])
    return api_response_data(Result.SUCCESS, {"event_detail": detail})


@log_info()
@validate_params_and_process_header(form=EventGetIdsSchema, data_format="JSON")
@verify_access_token()
def get_ids(request, data):
    from_ts = parse_string_to_timestamp(data["start_time"])
    to_ts = parse_string_to_timestamp(data["end_time"])
    if not from_ts or not to_ts or to_ts - from_ts > MAX_TIME_RANGE:
        return api_response_data(Result.ERROR_INVALID_TIME_RANGE)
    event_ids = event_manager.get_event_ids(from_ts, to_ts, data["channels"])
    return api_response_data(Result.SUCCESS, {"event_ids": event_ids})


@log_info()
@validate_params_and_process_header(form=EventGetIdsSchemaV2, data_format="JSON")
@verify_access_token()
def get_ids_v2(request, data):
    from_ts = parse_string_to_timestamp(data["start_time"])
    to_ts = parse_string_to_timestamp(data["end_time"])
    if not from_ts or not to_ts or to_ts - from_ts > MAX_TIME_RANGE:
        return api_response_data(Result.ERROR_INVALID_TIME_RANGE)
    event_ids = event_manager.get_event_ids_v2(from_ts, to_ts, data["channels"], data["from_id"], data["count"])
    return api_response_data(Result.SUCCESS, {"event_ids": event_ids})


@log_info()
@validate_params_and_process_header(form=EventGetInfosByIdsSchema, data_format="JSON")
@verify_access_token()
def get_infos_by_ids(request, data):
    event_ids = data["event_ids"]
    event_dict = event_manager.get_event_infos(event_ids)
    result = []
    for event_id in event_ids:
        if event_id not in event_dict:
            continue
        result.append(event_dict[event_id])
    return api_response_data(Result.SUCCESS, {"event_infos": result})


@log_info()
@validate_params_and_process_header(form=EventParticipateSchema, data_format="JSON")
@verify_access_token()
def participate(request, data):
    event_manager.participate_in_event(data["user_id"], data["event_id"])
    return api_response_data(Result.SUCCESS)
