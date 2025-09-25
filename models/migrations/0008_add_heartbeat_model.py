# Generated manually on 2025-09-25 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("models", "0007_add_symbol_to_strategy"),
    ]

    operations = [
        migrations.CreateModel(
            name="Heartbeat",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="models.account",
                    ),
                ),
                (
                    "strategy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="models.strategy",
                    ),
                ),
            ],
            options={
                "db_table": "heartbeats",
            },
        ),
    ]
