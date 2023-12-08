# Generated by Django 4.2.4 on 2023-09-13 23:59

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MainMenu",
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
                ("item", models.CharField(max_length=200, unique=True)),
                ("link", models.CharField(max_length=200, unique=True)),
            ],
        ),
    ]
