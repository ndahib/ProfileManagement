# Generated by Django 4.2.16 on 2024-11-01 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('avatar', models.CharField(max_length=255)),
                ('bio', models.TextField()),
                ('level', models.IntegerField()),
            ],
        ),
    ]