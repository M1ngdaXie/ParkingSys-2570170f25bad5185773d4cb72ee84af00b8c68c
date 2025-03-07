# Generated by Django 5.0.1 on 2024-04-05 02:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("driver", "0003_remove_permit_permit_type_permit_types"),
    ]

    operations = [
        migrations.AlterField(
            model_name="permit",
            name="types",
            field=models.CharField(
                choices=[
                    ("upermit", "UPermit"),
                    ("cupermit", "CUPermit"),
                    ("daypermit", "DayPermit"),
                ],
                max_length=50,
            ),
        ),
    ]
