# Generated by Django 4.0.6 on 2022-08-16 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CaseData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=250)),
                ('value', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='GeneralData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=250)),
                ('casename', models.CharField(max_length=250)),
                ('value', models.FloatField()),
            ],
        ),
    ]
