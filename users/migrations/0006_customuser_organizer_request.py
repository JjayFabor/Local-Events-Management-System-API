# Generated by Django 5.0.7 on 2024-07-30 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_customuser_is_organizer'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='organizer_request',
            field=models.BooleanField(default=False),
        ),
    ]