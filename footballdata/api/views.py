from rest_framework.decorators import api_view
from rest_framework.response import Response

from footballdata.api.tasks import ImportLeagueTask


@api_view(["GET"])
def import_league(request, league_code):
    t = ImportLeagueTask()
    t.delay(league_code)
    return Response(None)
