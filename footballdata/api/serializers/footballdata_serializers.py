from rest_framework import serializers


class CompetitionJSONSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=500)
    area_name = serializers.CharField(max_length=500)
    code = serializers.CharField(max_length=30)
    fd_id = serializers.IntegerField()  # Footballdata.org id

    def to_internal_value(self, initial_data):
        initial_data["area_name"] = initial_data.get("area", {}).get("name", None)
        initial_data["fd_id"] = initial_data.get("id", None)
        return super().to_internal_value(initial_data)


class CoachJSONSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=500, allow_null=True, allow_blank=True)
    date_of_birth = serializers.DateTimeField(allow_null=True)
    nationality = serializers.CharField(max_length=500, allow_null=True, allow_blank=True)
    fd_id = serializers.IntegerField(allow_null=True)  # Footballdata.org id

    def to_internal_value(self, initial_data):
        initial_data["date_of_birth"] = initial_data.get("dateOfBirth", None)
        initial_data["fd_id"] = initial_data.get("id", None)
        return super().to_internal_value(initial_data)


class PlayerJSONSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=500, allow_null=True, allow_blank=True)
    position = serializers.CharField(max_length=500, allow_null=True, allow_blank=True)
    date_of_birth = serializers.DateTimeField(allow_null=True)
    nationality = serializers.CharField(max_length=500, allow_null=True, allow_blank=True)
    fd_id = serializers.IntegerField(allow_null=True)  # Footballdata.org id

    def to_internal_value(self, initial_data):
        initial_data["date_of_birth"] = initial_data.get("dateOfBirth", None)
        initial_data["fd_id"] = initial_data.get("id", None)
        return super().to_internal_value(initial_data)


class TeamJSONSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=500)
    tla = serializers.CharField(max_length=30, allow_null=True, allow_blank=True)
    short_name = serializers.CharField(max_length=500, allow_null=True, allow_blank=True)
    area_name = serializers.CharField(max_length=500)
    address = serializers.CharField(max_length=500, allow_null=True, allow_blank=True)
    fd_id = serializers.IntegerField(allow_null=True)  # Footballdata.org id
    coach = CoachJSONSerializer()
    squad = PlayerJSONSerializer(many=True)

    def to_internal_value(self, initial_data):
        initial_data["area_name"] = initial_data.get("area", {}).get("name", None)
        initial_data["short_name"] = initial_data.get("shortName", None)
        initial_data["fd_id"] = initial_data.get("id", None)
        return super().to_internal_value(initial_data)
