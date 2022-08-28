from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from footballdata.api.models.footballdata_models import Competition, Player
from footballdata.api.serializers.footballdata_serializers import PlayerSerializer
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


class CompetitionPlayersList(generics.ListAPIView):
    serializer_class = PlayerSerializer

    def get_queryset(self):
        league_code = self.kwargs.get("league_code").upper()
        if not Competition.objects.filter(code=league_code).exists():
            raise NotFound("League not found.")
        queryset = Player.objects.get_queryset()
        queryset = queryset.filter(team__competitions__code=league_code)
        team_name = self.request.GET.get("team_name", None)
        if team_name:
            queryset = queryset.filter(team__name__icontains=team_name)
        return queryset
