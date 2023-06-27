from django.db import models
from users.models import User


class JournalDiaryModel(models.Model):
    name = models.TextField(max_length=255)
    description = models.TextField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class JournalSectionModel(models.Model):
    name = models.TextField(max_length=255)
    description = models.TextField(max_length=255)
    journal = models.ForeignKey(JournalDiaryModel, on_delete=models.CASCADE)
    background = models.TextField(max_length=255, default="")


class JournalSectionEntriesModel(models.Model):
    name = models.TextField(max_length=255)
    description = models.TextField(max_length=255)
    journalSection = models.ForeignKey(JournalSectionModel, on_delete=models.CASCADE)
    content = models.TextField()
