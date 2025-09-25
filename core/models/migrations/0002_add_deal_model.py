# Generated manually on 2025-09-25 17:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("models", "0001_initial_strategy"),
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
                ("strategy_prefix", models.CharField(max_length=50)),
                ("time", models.DateTimeField()),
                ("symbol", models.CharField(max_length=100)),
                ("type", models.CharField(max_length=50)),
                ("direction", models.IntegerField()),
                (
                    "volume",
                    models.DecimalField(decimal_places=8, max_digits=20),
                ),
                (
                    "price",
                    models.DecimalField(decimal_places=8, max_digits=20),
                ),
                (
                    "profit",
                    models.DecimalField(
                        blank=True,
                        decimal_places=8,
                        max_digits=20,
                        null=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "deals",
            },
        ),
    ]
