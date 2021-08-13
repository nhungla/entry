from entry_task.views.form_schema import AdminCreateEventSchema
from event_lib.managers import event_manager
from event_lib.constants import Result
from event_lib.verify_access_token import verify_access_token
from event_lib.utils import validate_params_and_process_header, api_response_data, \
    parse_string_to_timestamp, log_info


@log_info()
@validate_params_and_process_header(form=AdminCreateEventSchema, data_format="JSON")
@verify_access_token(is_required_admin=True)
def create_event(request, data):
    start_time = parse_string_to_timestamp(data["start_time"])
    end_time = parse_string_to_timestamp(data["end_time"])
    if not start_time or not end_time or start_time >= end_time:
        return api_response_data(Result.ERROR_INVALID_TIME_RANGE)
    event_id = event_manager.\
        create_event(data["user_id"], start_time, end_time, data["channel"],
                     data["name"], data["description"], data["location"], data["image_url"])
    return api_response_data(Result.SUCCESS, {"event_id": event_id})
