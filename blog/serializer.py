from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from blog.models import BlogPostModel, BlogLikeModel, BlogCommentsModel, TagsModel, BlogTagModel


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagsModel
        fields = "__all__"


class BlogTagSerializer(serializers.ModelSerializer):
    tag = TagsSerializer

    class Meta:
        model = BlogTagModel
        fields = "__all__"


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPostModel
        fields = "__all__"


class BlogLikeDisLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogLikeModel
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(
                queryset=BlogLikeModel.objects.all(),
                fields=['post', 'sender']
            )
        ]


class BlogCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCommentsModel
        fields = "__all__"
