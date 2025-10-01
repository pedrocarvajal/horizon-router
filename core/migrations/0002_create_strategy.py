# Generated manually on 2025-10-01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_create_account"),
    ]

    operations = [
        migrations.CreateModel(
            name="Strategy",
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
                ("name", models.CharField(max_length=255)),
                ("prefix", models.CharField(max_length=50)),
                ("symbol", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "strategies",
            },
        ),
    ]
