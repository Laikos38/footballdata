from django.urls import path

from footballdata.api.views import CompetitionPlayersList, TeamsByName, import_league

urlpatterns = [
    path("import-league/<str:league_code>/", import_league),
    path("competitions/<str:league_code>/players/", CompetitionPlayersList.as_view()),
    path("teams/", TeamsByName.as_view()),
]
