from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from footballdata.api.models.common_models import TimeStampModel


class CeleryTask(TimeStampModel):
    PENDING = "PENDING"
    RECEIVED = "RECEIVED"
    STARTED = "STARTED"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    REVOKED = "REVOKED"
    REJECTED = "REJECTED"
    RETRY = "RETRY"
    IGNORED = "IGNORED"
    STATES = (
        (PENDING, PENDING),
        (RECEIVED, RECEIVED),
        (STARTED, STARTED),
        (SUCCESS, SUCCESS),
        (FAILURE, FAILURE),
        (REVOKED, REVOKED),
        (REJECTED, REJECTED),
        (RETRY, RETRY),
        (IGNORED, IGNORED),
    )

    task_id = models.CharField(max_length=500)
    task_name = models.CharField(max_length=500)
    status = models.CharField(max_length=50, choices=STATES, default=PENDING)
    result_data = models.JSONField(null=True, blank=True, encoder=DjangoJSONEncoder)

    class Meta:
        db_table = "celery_tasks"
        ordering = ("-created",)
