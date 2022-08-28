import datetime

from celery import Task

from footballdata.api.models.celery_models import CeleryTask


class CallbackTask(Task):
    task_instance: CeleryTask | None = None

    def on_success(self, retval, task_id, args, kwargs):
        if self.task_instance:
            self.task_instance.status = CeleryTask.SUCCESS
            self.task_instance.save()
        super().on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        if self.task_instance:
            self.task_instance.status = CeleryTask.FAILURE
            self.task_instance.save()
        super().on_failure(exc, task_id, args, kwargs, einfo)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        if self.task_instance:
            result_data = {
                "status": status,
                "task_id": task_id,
                "task_name": self.name,
                "result": retval,
                "args": args,
                "kwargs": kwargs,
                "traceback": self.AsyncResult(task_id).traceback,
                "date_done": self.AsyncResult(task_id).date_done,
            }
            if status not in (CeleryTask.SUCCESS, CeleryTask.FAILURE):
                self.task_instance.status = status
            self.task_instance.result_data = result_data
            self.task_instance.save()


def create_celery_task(task_id, task_name):
    return CeleryTask.objects.create(task_id=task_id, task_name=task_name, status=CeleryTask.PENDING)


def exists_active_task(task_name, time_span=None) -> tuple[bool, str | None]:
    time_span = time_span or datetime.datetime.now() - datetime.timedelta(minutes=2)
    active_task = (
        CeleryTask.objects.filter(
            task_name=task_name, status__in=[CeleryTask.PENDING, CeleryTask.RECEIVED, CeleryTask.STARTED, CeleryTask.RETRY]
        )
        .exclude(created__lt=time_span)
        .first()
    )
    return active_task is not None, active_task.task_id if active_task else None
