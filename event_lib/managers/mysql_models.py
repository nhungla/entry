from django.db import models


class EventDB:
    class EntryTaskDbConfig:
        class Config:
            db_for_write = "entry_task_db.master"

    class EventTab(models.Model, EntryTaskDbConfig):
        id = models.BigAutoField(primary_key=True)
        create_uid = models.PositiveIntegerField()
        create_time = models.PositiveIntegerField()
        start_time = models.PositiveIntegerField()
        end_time = models.PositiveIntegerField()
        channel = models.PositiveSmallIntegerField()
        extra_data = models.TextField()
        """
        extra_data contains:
            required: image_url = models.CharField(max_length=255)
            required: location = models.CharField(max_length=255)
            required: description = models.TextField(null=True)
            required: name = models.CharField(max_length=255)
        """

        class Meta:
            db_table = 'event_tab'

    class UserTab(models.Model, EntryTaskDbConfig):
        id = models.BigAutoField(primary_key=True)
        user_name = models.CharField(max_length=255)
        salt = models.CharField(max_length=20)
        password_hash = models.CharField(max_length=255)
        user_type = models.PositiveSmallIntegerField()

        class Meta:
            db_table = 'user_tab'

    class EventParticipantTab(models.Model, EntryTaskDbConfig):
        id = models.PositiveIntegerField(primary_key=True)
        user_id = models.PositiveIntegerField()
        event_id = models.PositiveIntegerField()

        class Meta:
            db_table = "event_participant_tab"

    class EventLikeTab(models.Model, EntryTaskDbConfig):
        id = models.BigAutoField(primary_key=True)
        user_id = models.PositiveIntegerField()
        event_id = models.PositiveIntegerField()

        class Meta:
            db_table = "event_like_tab"

    class EventCommentTab(models.Model, EntryTaskDbConfig):
        id = models.BigAutoField(primary_key=True)
        user_id = models.PositiveIntegerField()
        event_id = models.PositiveIntegerField()
        extra_data = models.TextField()

        class Meta:
            db_table = "event_comment_tab"
