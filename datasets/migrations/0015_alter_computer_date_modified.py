# Generated by Django 4.0.6 on 2022-07-09 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0014_computer_date_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computer',
            name='date_modified',
            field=models.DateTimeField(),
        ),
    ]