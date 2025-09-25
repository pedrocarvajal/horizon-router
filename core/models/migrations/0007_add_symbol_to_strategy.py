# Generated manually on 2025-09-25 17:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("models", "0006_add_snapshot_model"),
    ]

    operations = [
        migrations.AddField(
            model_name="strategy",
            name="symbol",
            field=models.CharField(max_length=100),
            preserve_default=False,
        ),
    ]
