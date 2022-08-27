from django.urls import path

from footballdata.api.views import import_league

urlpatterns = [
    path("import-league/<str:league_code>/", import_league),
]
