# Generated by Django 4.0.6 on 2022-08-10 07:56

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('georepo', '0012_dataset_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4),
        ),
    ]
