from entry_task.views.form_schema import MediaUploadImageSchema
from event_lib.managers import media_manager
from event_lib.constants import Result
from event_lib.verify_access_token import verify_access_token
from event_lib.utils import validate_params_and_process_header, api_response_data, log_info

VALID_IMAGE_EXTENSIONS = frozenset([
    "png",
    "jpg",
])


@log_info()
@validate_params_and_process_header(form=MediaUploadImageSchema, data_format="JSON")
@verify_access_token()
def upload_image(request, data):
    image_name = data["image_name"]
    image_content = data["image_content"]
    extension = image_name.split(".")[-1].strip().lower()
    if extension not in VALID_IMAGE_EXTENSIONS:
        return api_response_data(Result.ERROR_INVALID_IMAGE)
    file_name = media_manager.save_image(image_content, extension)
    if not file_name:
        return api_response_data(Result.ERROR_SOMETHING_WRONG)
    return api_response_data(Result.SUCCESS, {"file_name": file_name})
