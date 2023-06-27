from django.db import models
from django.contrib.auth.models import User


class UserDetailModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userDetail')
    image = models.TextField(max_length=500, blank=True)
