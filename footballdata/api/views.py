from rest_framework.decorators import api_view
from rest_framework.response import Response

from footballdata.api.services.celery_service import exists_active_task
from footballdata.api.services.footballdataorg_service import FootballDataOrgService
from footballdata.api.tasks import ImportLeagueTask


@api_view(["GET"])
def import_league(request, league_code: str):
    sync = request.GET.get("sync", False)
    if not sync:
        t = ImportLeagueTask()
        exists, task_id = exists_active_task(t.name)
        if exists:
            return Response(f"Already importing process running. Wait until process finish. Task id = {task_id}", 200)
        async_result = t.delay(league_code)
        return Response(f"Import process started. Task id = {async_result.id}")
    else:
        service = FootballDataOrgService()
        result, message = service.import_competition(league_code)
        return Response(message, 201 if result else 500)
