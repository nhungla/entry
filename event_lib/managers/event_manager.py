from django.db import IntegrityError
from event_lib.managers.mysql_models import *
from event_lib.managers.cache_manager import cache_data_by_keys, CACHE_KEY_FUNC_GET_EVENT_INFOS_BY_IDS, \
    one_key_cache_data, CACHE_KEY_FUNC_GET_EVENT_DETAIL_BY_ID, remove_key_cache
from event_lib.managers import user_manager
import event_lib.utils as ut


def create_event(create_uid, start_time, end_time, channel, location, name, image_url, description):
    extra_data = {
        "location": location,
        "name": name,
        "image_url": image_url,
        "description": description,
    }
    model = EventDB.EventTab.objects.create(
        create_uid=create_uid,
        create_time=ut.get_timestamp(),
        start_time=start_time,
        end_time=end_time,
        channel=channel,
        extra_data=ut.to_json(extra_data)
    )
    return model.id


def comment_on_event(user_id, event_id, comment_detail):
    try:
        EventDB.EventCommentTab.objects.create(
            event_id=event_id,
            user_id=user_id,
            extra_data=ut.to_json({
                "comment": comment_detail,
            })
        )
        remove_key_cache(CACHE_KEY_FUNC_GET_EVENT_DETAIL_BY_ID["cache_prefix"] % event_id)
    except IntegrityError:
        pass


@one_key_cache_data(**CACHE_KEY_FUNC_GET_EVENT_DETAIL_BY_ID)
def get_detail(event_id):
    result = {}
    participate_ids_set = set(EventDB.EventParticipantTab.objects.filter(event_id=event_id).values_list("user_id", flat=True))
    user_ids_set = set(participate_ids_set)
    user_like_ids_set = set(EventDB.EventLikeTab.objects.filter(event_id=event_id).values_list("user_id", flat=True))
    comments = list(EventDB.EventCommentTab.objects.filter(event_id=event_id).values())
    user_ids_set.update({comment["user_id"] for comment in comments})
    user_ids_set.update(user_like_ids_set)
    user_info_dict = user_manager.get_user_infos_by_ids(list(user_ids_set))
    participant_list = []
    for user_id in participate_ids_set:
        user_info = user_info_dict.get(user_id)
        if not user_info:
            continue
        participant_list.append({
            "user_id": user_id,
            "user_name": user_info["user_name"],
        })
    result["participants"] = participant_list

    user_like_list = []
    for user_id in user_like_ids_set:
        user_info = user_info_dict.get(user_id)
        if not user_info:
            continue
        user_like_list.append({
            "user_id": user_id,
            "user_name": user_info["user_name"]
        })
    result["user_like_infos"] = user_like_list

    comment_list = []
    for comment in comments:
        extra_data = comment.pop("extra_data")
        extra_data = ut.from_json(extra_data)
        user_id = comment["user_id"]
        comment_list.append({
            "user_id": user_id,
            "user_name": user_info_dict.get(user_id, {}).get("user_name", ""),
            "comment": extra_data["comment"]
        })
    result["comments"] = comment_list

    return result


def get_event_ids(from_time, to_time, channels):
    result = list(EventDB.EventTab.objects.filter(start_time__lte=from_time, end_time__gte=to_time,
                                                  channel__in=channels).values_list("id", flat=True))
    return result


@cache_data_by_keys(**CACHE_KEY_FUNC_GET_EVENT_INFOS_BY_IDS)
def get_event_infos(event_ids):
    models = list(EventDB.EventTab.objects.filter(id__in=event_ids).values())
    result = {}
    for model in models:
        extra_data = model.pop("extra_data")
        extra_data = ut.from_json(extra_data)
        model.update({
            "location": extra_data["location"],
            "description": extra_data["description"],
            "image_url": extra_data["image_url"],
            "name": extra_data["name"],
        })
        result[model["id"]] = model
    return result


def like_event(user_id, event_id):
    try:
        EventDB.EventLikeTab.objects.create(
            event_id=event_id,
            user_id=user_id
        )
        remove_key_cache(CACHE_KEY_FUNC_GET_EVENT_DETAIL_BY_ID["cache_prefix"] % event_id)
    except IntegrityError:
        pass


def participate_in_event(user_id, event_id):
    try:
        EventDB.EventParticipantTab.objects.create(
            event_id=event_id,
            user_id=user_id
        )
        remove_key_cache(CACHE_KEY_FUNC_GET_EVENT_DETAIL_BY_ID["cache_prefix"] % event_id)
    except IntegrityError:
        pass
