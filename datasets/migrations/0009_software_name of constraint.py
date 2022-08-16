# Generated by Django 4.0.6 on 2022-07-08 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0008_remove_software_name of constraint'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='software',
            constraint=models.UniqueConstraint(fields=('name', 'version'), name='name of constraint'),
        ),
    ]