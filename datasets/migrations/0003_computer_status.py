# Generated by Django 4.0.6 on 2022-07-07 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0002_alter_computer_options_computer_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='computer',
            name='status',
            field=models.CharField(default='ok', max_length=30),
            preserve_default=False,
        ),
    ]