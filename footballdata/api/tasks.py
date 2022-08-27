from footballdata.api.services.footballdataorg_service import import_competition
from footballdata.celery import app


@app.task()
def import_league_task(league_code: str):
    import_competition(league_code)
