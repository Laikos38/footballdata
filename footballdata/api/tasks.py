from footballdata.api.services.celery_service import CallbackTask, create_celery_task
from footballdata.api.services.footballdataorg_service import import_competition
from footballdata.celery import app


class ImportLeagueTask(CallbackTask):
    name = "import_league_task"

    def run(self, league_code, *args, **kwargs):
        self.task_instance = create_celery_task(self.request.id, self.name)
        import_competition(league_code)


app.register_task(ImportLeagueTask())
