# Generated manually on 2025-09-25 17:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("models", "0008_add_heartbeat_model"),
    ]

    operations = [
        migrations.AlterField(
            model_name="strategy",
            name="prefix",
            field=models.CharField(max_length=50),
        ),
    ]
