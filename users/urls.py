from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserCreateAPIView, UserRetrieveUpdateApiView, UserUploadPictureApiView

urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup', UserCreateAPIView.as_view(), name="user_signup"),
    path('action', UserRetrieveUpdateApiView.as_view()),
    path('upload/picture', UserUploadPictureApiView.as_view()),
]
