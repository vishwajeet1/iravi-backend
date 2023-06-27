import enum

from django.db import models
from users.models import User


class TagsModel(models.Model):
    tagName = models.TextField(max_length=255)


class BlogPostModel(models.Model):
    postText = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class BlogTagModel(models.Model):
    tag = models.ForeignKey(TagsModel, on_delete=models.CASCADE)
    blog = models.ForeignKey(BlogPostModel, on_delete=models.CASCADE)


class BlogLikeModel(models.Model):
    blog = models.ForeignKey(BlogPostModel, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')


class BlogCommentsModel(models.Model):
    blog = models.ForeignKey(BlogPostModel, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    comment = models.TextField(max_length=255)
