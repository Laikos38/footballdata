from django.db import models

from footballdata.api.models.common_models import TimeStampModel


class Competition(TimeStampModel):
    name = models.CharField(max_length=500)
    area_name = models.CharField(max_length=500)
    code = models.CharField(max_length=30)
    fd_id = models.IntegerField()  # Footballdata.org id

    class Meta:
        indexes = [
            models.Index(fields=["code"]),
        ]
        db_table = "competitions"
        ordering = ("created",)


class Team(TimeStampModel):
    name = models.CharField(max_length=500)
    tla = models.CharField(max_length=30, blank=True, null=True)
    short_name = models.CharField(max_length=500, blank=True, null=True)
    area_name = models.CharField(max_length=500)
    address = models.CharField(max_length=500, blank=True, null=True)
    fd_id = models.IntegerField()  # Footballdata.org id

    competitions = models.ManyToManyField(Competition, related_name="teams")

    class Meta:
        db_table = "teams"
        ordering = ("created",)


class Coach(TimeStampModel):
    name = models.CharField(max_length=500, blank=True, null=True)
    date_of_birth = models.DateTimeField(null=True)
    nationality = models.CharField(max_length=500, blank=True, null=True)
    fd_id = models.IntegerField(null=True)  # Footballdata.org id

    team = models.ForeignKey(Team, related_name="coaches", on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "coaches"
        ordering = ("created",)


class Player(TimeStampModel):
    name = models.CharField(max_length=500, blank=True, null=True)
    position = models.CharField(max_length=500, blank=True, null=True)
    date_of_birth = models.DateTimeField(null=True)
    nationality = models.CharField(max_length=500, blank=True, null=True)
    fd_id = models.IntegerField()  # Footballdata.org id

    team = models.ForeignKey(Team, related_name="players", on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "players"
        ordering = ("created",)
