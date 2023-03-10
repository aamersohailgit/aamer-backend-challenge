# Generated by Django 4.1.5 on 2023-01-26 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("person", "0002_person_address"),
    ]

    operations = [
        migrations.AlterField(
            model_name="address",
            name="state",
            field=models.CharField(
                choices=[
                    ("NSW", "NSW"),
                    ("VIC", "VIC"),
                    ("QLD", "QLD"),
                    ("SA", "SA"),
                    ("WA", "WA"),
                    ("TAS", "TAS"),
                    ("NT", "NT"),
                    ("ACT", "ACT"),
                ],
                max_length=255,
            ),
        ),
    ]
