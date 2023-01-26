# Generated by Django 4.1.5 on 2023-01-26 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("person", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="address",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="person",
                to="person.address",
            ),
            preserve_default=False,
        ),
    ]
