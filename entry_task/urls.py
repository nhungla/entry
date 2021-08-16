from django.conf.urls import url
from entry_task.views import admin_api, event_api, user_api, media_api


urlpatterns = [
    url(r'^api/admin/create_event$', admin_api.create_event),

    url(r'^api/event/comment$', event_api.comment),
    url(r'^api/event/get_detail$', event_api.get_detail),
    url(r'^api/event/get_ids$', event_api.get_ids),
    url(r'^api/event/get_infos_by_ids$', event_api.get_infos_by_ids),
    url(r'^api/event/like$', event_api.like),
    url(r'^api/event/participate$', event_api.participate),

    url(r'^api/media/upload_image$', media_api.upload_image),

    url(r'^api/user/create_user$', user_api.create_user),
    url(r'^api/user/login$', user_api.login),
    url(r'^api/user/pre_login$', user_api.pre_login),
]
