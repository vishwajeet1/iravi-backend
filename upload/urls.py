from django.urls import path

from upload.views import FileUploadView

urlpatterns = [
    path('profile', FileUploadView.as_view())
]
