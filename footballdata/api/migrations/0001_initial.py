# Generated by Django 4.1 on 2022-08-27 19:50

import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CeleryTask",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("task_id", models.CharField(max_length=500)),
                ("task_name", models.CharField(max_length=500)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "PENDING"),
                            ("RECEIVED", "RECEIVED"),
                            ("STARTED", "STARTED"),
                            ("SUCCESS", "SUCCESS"),
                            ("FAILURE", "FAILURE"),
                            ("REVOKED", "REVOKED"),
                            ("REJECTED", "REJECTED"),
                            ("RETRY", "RETRY"),
                            ("IGNORED", "IGNORED"),
                        ],
                        default="PENDING",
                        max_length=50,
                    ),
                ),
                ("result_data", models.JSONField(blank=True, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True)),
            ],
            options={
                "db_table": "celery_tasks",
                "ordering": ("-created",),
            },
        ),
    ]
