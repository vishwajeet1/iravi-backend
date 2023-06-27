from rest_framework import serializers
from journal_diary.models import JournalDiaryModel, JournalSectionModel, JournalSectionEntriesModel


class JournalDiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalDiaryModel
        fields = "__all__"


class JournalSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalSectionModel
        fields = "__all__"


class JournalSectionEntriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalSectionEntriesModel
        fields = "__all__"
