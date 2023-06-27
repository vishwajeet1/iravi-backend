from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from upload.service import uploadFileToS3Bucket
from .models import User, UserDetailModel
from .serializer import UserSerializer, UserDetailSerializer

# Create your views here.
from rest_framework import viewsets, generics, permissions, status


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer = UserSerializer()


class UserCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserRetrieveUpdateApiView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.pk)
        return obj

    def update(self, request, *args, **kwargs):
        pk = request.user.pk
        userInstance = self.get_object()
        detailInstance, created = UserDetailModel.objects.all().get_or_create(user_id=pk)
        detailSerializer = UserDetailSerializer(instance=detailInstance, data=request.data, partial=True)
        userSerializer = self.serializer_class(instance=userInstance, data=request.data, partial=True)
        if userSerializer.is_valid() and detailSerializer.is_valid():
            userSerializer.save()
            detailSerializer.save()
            return Response({**userSerializer.data})
        return Response(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUploadPictureApiView(generics.UpdateAPIView):
    serializer_class = UserDetailSerializer
    queryset = UserDetailModel.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj, created = queryset.get_or_create(user=self.request.user.pk)
        return obj

    def update(self, request, *args, **kwargs):
        file = request.data
        uploadData = uploadFileToS3Bucket(file, "profile/")
        if uploadData.get("success"):
            request.data["image"] = uploadData.get("url")
            detailSerializer = UserDetailSerializer(instance=self.get_object(), data=request.data,
                                                    partial=True)
            if detailSerializer.is_valid():
                detailSerializer.save()
                return Response(detailSerializer.data)
            else:
                return Response(detailSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(uploadData.get("error"), status=status.HTTP_400_BAD_REQUEST)
