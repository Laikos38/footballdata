from rest_framework.decorators import api_view
from rest_framework.response import Response

from footballdata.api.tasks import import_league_task


@api_view(["GET"])
def import_league(request, league_code):
    import_league_task.delay(league_code)
    return Response(None)
