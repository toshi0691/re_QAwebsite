# Generated by Django 4.0.4 on 2022-06-10 02:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'permissions': (('is_activated', 'User is activated'),), 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]
