# Generated by Django 4.2.4 on 2023-12-06 23:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("bookMng", "0005_alter_comment_book"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="current_owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="current_owner",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
