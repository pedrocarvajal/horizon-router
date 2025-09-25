# Generated manually on 2025-09-25 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("models", "0004_add_account_to_deal"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="deal",
            name="strategy_prefix",
        ),
        migrations.AddField(
            model_name="deal",
            name="strategy",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="models.strategy",
            ),
            preserve_default=False,
        ),
    ]
