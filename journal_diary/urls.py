from django.urls import path

from journal_diary.views import JournalDiaryListCreateView, JournalSectionListCreateView, JournalDiaryDetailView

urlpatterns = [
    path('journal', JournalDiaryListCreateView.as_view()),
    path('journal/<int:pk>', JournalDiaryDetailView.as_view()),
    path('journal/<int:pk>/section', JournalSectionListCreateView.as_view()),
]
