from time import sleep

import requests
from django.conf import settings
from django.db import transaction

from footballdata.api.models.footballdata_models import Coach, Competition, Player, Team
from footballdata.api.serializers.footballdata_serializers import (
    CompetitionJSONSerializer,
    TeamJSONSerializer,
)

FOOTBALLDATAORG_BASE_URL = "http://api.football-data.org/v4"


class FootballDataOrgService:
    def __init__(self) -> None:
        if not settings.FOOTBALLDATAORG_API_KEY:
            raise Exception("API KEY NOT FOUND.")
        self.session: requests.Session = requests.session()
        self.session.headers = {"X-Auth-Token": settings.FOOTBALLDATAORG_API_KEY}  # type: ignore

    def request(self, url) -> requests.Response:
        while True:
            response = self.session.get(url)
            if response.status_code == 429:
                sleep(40)
                continue
            if response.status_code == 403:
                raise Exception(
                    "The resource you are looking for is restricted and apparently not within your permissions. Please check your subscription."
                )
            if response.status_code != 200:
                raise Exception("Error during request to football-data.org API.")
            break
        return response

    def import_competition(self, league_code: str, update_existing_instances=False):
        league_code = league_code.upper()
        try:
            competition_response = self.request(f"{FOOTBALLDATAORG_BASE_URL}/competitions/{league_code}")
            teams_response = self.request(f"{FOOTBALLDATAORG_BASE_URL}/competitions/{league_code}/teams")
        except Exception as e:
            return False, str(e)
        competition_instance = Competition.objects.filter(code=league_code).first()
        competition = CompetitionJSONSerializer(data=competition_response.json())
        competition.is_valid(raise_exception=True)
        teams_response_dict: dict = teams_response.json()
        teams = TeamJSONSerializer(data=teams_response_dict.get("teams"), many=True)
        teams.is_valid(raise_exception=True)
        team_instances = []
        with transaction.atomic():
            if not competition_instance:
                competition_instance = Competition.objects.create(
                    name=competition.validated_data.get("name"),
                    area_name=competition.validated_data.get("area_name"),
                    code=competition.validated_data.get("code"),
                    fd_id=competition.validated_data.get("fd_id"),
                )
            elif update_existing_instances:
                competition_instance.name = competition.validated_data.get("name")
                competition_instance.area_name = competition.validated_data.get("area_name")
                competition_instance.code = competition.validated_data.get("code")
                competition_instance.fd_id = competition.validated_data.get("fd_id")
                competition_instance.save()
            for team in teams.validated_data:
                try:
                    team_instance = Team.objects.filter(fd_id=team.get("fd_id")).first()
                    ignore_coach_players = True
                    if not team_instance:
                        ignore_coach_players = False
                        team_instance = Team.objects.create(
                            name=team.get("name"),
                            tla=team.get("tla"),
                            short_name=team.get("short_name"),
                            area_name=team.get("area_name"),
                            address=team.get("address"),
                            fd_id=team.get("fd_id"),
                        )
                    elif update_existing_instances:
                        ignore_coach_players = False
                        team_instance.name = team.get("name")
                        team_instance.tla = team.get("tla")
                        team_instance.short_name = team.get("short_name")
                        team_instance.area_name = team.get("area_name")
                        team_instance.address = team.get("address")
                        team_instance.fd_id = team.get("fd_id")
                        team_instance.save()
                    team_instances.append(team_instance)
                    if ignore_coach_players:
                        continue
                    coach_instance = Coach.objects.filter(team=team_instance).first()
                    coach_data = team.get("coach")
                    if not coach_instance:
                        Coach.objects.create(
                            name=coach_data.get("name"),
                            date_of_birth=coach_data.get("date_of_birth"),
                            nationality=coach_data.get("nationality"),
                            fd_id=coach_data.get("fd_id"),
                            team=team_instance,
                        )
                    elif update_existing_instances:
                        coach_instance.name = coach_data.get("name")
                        coach_instance.date_of_birth = coach_data.get("date_of_birth")
                        coach_instance.nationality = coach_data.get("nationality")
                        coach_instance.fd_id = coach_data.get("fd_id")
                        coach_instance.team = team_instance
                        coach_instance.save()
                    if not len(team.get("squad")):
                        continue
                    for player in team.get("squad"):
                        player_instance = Player.objects.filter(fd_id=player.get("fd_id")).first()
                        if not player_instance:
                            Player.objects.create(
                                name=player.get("name"),
                                position=player.get("position"),
                                date_of_birth=player.get("date_of_birth"),
                                nationality=player.get("nationality"),
                                fd_id=player.get("fd_id"),
                                team=team_instance,
                            )
                        elif update_existing_instances:
                            player_instance.name = player.get("name")
                            player_instance.position = player.get("position")
                            player_instance.date_of_birth = player.get("date_of_birth")
                            player_instance.nationality = player.get("nationality")
                            player_instance.fd_id = player.get("fd_id")
                            player_instance.team = team_instance
                            player_instance.save()
                except Exception as e:
                    print(e)
            if team_instances:
                transaction.on_commit(lambda: competition_instance.teams.add(*team_instances))  # type: ignore
        return True, "Success"
