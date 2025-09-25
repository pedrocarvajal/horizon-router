# Generated manually on 2025-09-25 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("models", "0003_add_account_model"),
    ]

    operations = [
        migrations.AddField(
            model_name="deal",
            name="account",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="models.account",
            ),
            preserve_default=False,
        ),
    ]
