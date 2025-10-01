# Generated manually on 2025-10-01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_create_strategy"),
    ]

    operations = [
        migrations.CreateModel(
            name="Snapshot",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("event", models.CharField(max_length=255)),
                ("balance", models.DecimalField(decimal_places=8, max_digits=20)),
                ("nav", models.DecimalField(decimal_places=8, max_digits=20)),
                ("exposure", models.DecimalField(decimal_places=8, max_digits=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.account"
                    ),
                ),
                (
                    "strategy",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.strategy",
                    ),
                ),
            ],
            options={
                "db_table": "snapshots",
            },
        ),
    ]
