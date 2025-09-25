# Generated manually on 2025-09-25 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("models", "0005_change_strategy_prefix_to_fk"),
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
                (
                    "nav",
                    models.DecimalField(decimal_places=8, max_digits=20),
                ),
                (
                    "exposure",
                    models.DecimalField(decimal_places=8, max_digits=20),
                ),
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
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="models.strategy",
                    ),
                ),
            ],
            options={
                "db_table": "snapshots",
            },
        ),
    ]
