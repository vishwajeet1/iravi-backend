from django.contrib.auth.hashers import make_password

from .models import User, UserDetailModel
from rest_framework import serializers


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetailModel
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # userDetail = UserDetailSerializer(many=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'username']

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
