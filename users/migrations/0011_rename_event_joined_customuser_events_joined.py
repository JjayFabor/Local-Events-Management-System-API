# Generated by Django 5.0.7 on 2024-08-02 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_remove_customuser_is_registered_event'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='event_joined',
            new_name='events_joined',
        ),
    ]