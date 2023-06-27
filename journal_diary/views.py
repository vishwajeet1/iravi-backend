from rest_framework import generics
from rest_framework.response import Response

from journal_diary.models import JournalDiaryModel, JournalSectionModel
from journal_diary.serializer import JournalDiarySerializer, JournalSectionSerializer


# Create your views here.

class JournalDiaryListCreateView(generics.ListCreateAPIView):
    queryset = JournalDiaryModel.objects.all()
    serializer_class = JournalDiarySerializer

    def post(self, request, *args, **kwargs):
        request.data["author"] = request.user.pk
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user.pk)


class JournalDiaryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JournalDiaryModel.objects.all()
    serializer_class = JournalDiarySerializer

    # def patch(self, request, *args, **kwargs):
    #     return self.partial_update(request, *args, **kwargs)

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user.pk)

    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        instance = self.get_object()
        journalDiarySerializer = self.get_serializer(instance)
        extraData = {}
        journalSection = JournalSectionModel.objects.all()
        extraData["sections"] = JournalSectionSerializer(journalSection.filter(journal=pk), many=True).data
        responseData = journalDiarySerializer.data
        responseData.update(extraData)
        return Response(responseData)


class JournalSectionListCreateView(generics.ListCreateAPIView):
    queryset = JournalSectionModel.objects.all()
    serializer_class = JournalSectionSerializer

    def post(self, request, *args, **kwargs):
        request.data["journal"] = kwargs["pk"]
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        return self.queryset.filter(journal=self.kwargs["pk"])
