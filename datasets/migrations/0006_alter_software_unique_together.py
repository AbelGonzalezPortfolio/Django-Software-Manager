# Generated by Django 4.0.6 on 2022-07-08 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0005_computer_software'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='software',
            unique_together={('name', 'version')},
        ),
    ]
