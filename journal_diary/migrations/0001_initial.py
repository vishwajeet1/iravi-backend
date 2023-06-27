# Generated by Django 4.1.7 on 2023-06-19 17:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JournalDiaryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=255)),
                ('description', models.TextField(max_length=255)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='JournalSectionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=255)),
                ('description', models.TextField(max_length=255)),
                ('background', models.TextField(max_length=255)),
                ('journal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='journal_diary.journaldiarymodel')),
            ],
        ),
        migrations.CreateModel(
            name='JournalSectionEntriesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=255)),
                ('description', models.TextField(max_length=255)),
                ('content', models.TextField()),
                ('journalSection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='journal_diary.journalsectionmodel')),
            ],
        ),
    ]
