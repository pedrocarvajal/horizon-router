# Generated manually on 2025-10-01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_create_heartbeat"),
    ]

    operations = [
        migrations.CreateModel(
            name="Deal",
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
                ("token", models.CharField(max_length=255)),
                ("time", models.DateTimeField()),
                ("symbol", models.CharField(max_length=100)),
                ("type", models.CharField(max_length=50)),
                ("direction", models.IntegerField()),
                ("volume", models.DecimalField(decimal_places=8, max_digits=20)),
                ("price", models.DecimalField(decimal_places=8, max_digits=20)),
                (
                    "profit",
                    models.DecimalField(
                        blank=True, decimal_places=8, max_digits=20, null=True
                    ),
                ),
                (
                    "take_profit_price",
                    models.DecimalField(
                        blank=True, decimal_places=8, max_digits=20, null=True
                    ),
                ),
                (
                    "stop_loss_price",
                    models.DecimalField(
                        blank=True, decimal_places=8, max_digits=20, null=True
                    ),
                ),
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
                        on_delete=django.db.models.deletion.CASCADE, to="core.strategy"
                    ),
                ),
            ],
            options={
                "db_table": "deals",
            },
        ),
    ]
