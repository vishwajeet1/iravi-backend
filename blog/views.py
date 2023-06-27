from django.db.models import Prefetch
from rest_framework import generics, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.exceptions import APIException

from blog.models import BlogLikeModel, BlogPostModel, BlogCommentsModel, TagsModel, BlogTagModel
from blog.serializer import BlogLikeDisLikeSerializer, BlogPostSerializer, \
    BlogCommentSerializer, BlogTagSerializer

from users.models import User


class BlogListCreateView(generics.ListCreateAPIView):
    queryset = BlogPostModel.objects.all()
    serializer_class = BlogPostSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        tagsData = self.request.data.get('tags', None)
        for tagData in tagsData:
            tag, created = TagsModel.objects.get_or_create(tagName=tagData)
            BlogTagModel.objects.create(blog=instance, tag=tag)
        return instance

    def post(self, request, *args, **kwargs):
        request.data["author"] = request.user.pk
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        userPosts = super().list(request, args, kwargs)
        postLike = BlogLikeModel.objects.all()
        postComments = BlogCommentsModel.objects.all()
        tagObj = TagsModel \
            .objects.all()
        for userPost in userPosts.data:
            userPost["likes"] = len(postLike.filter(blog=userPost["id"]))
            userPost["comments"] = len(postComments.filter(blog=userPost["id"]))
            userPost["tags"] = tagObj.filter(blogtagmodel__blog=userPost["id"]).values_list('tagName', flat=True)
        return Response(userPosts.data)


class BlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPostModel.objects.all()
    serializer_class = BlogPostSerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        instance = self.get_object()
        blogPostSerializer = self.get_serializer(instance)
        extraData = {}
        postLike = BlogLikeModel.objects.all()
        postComments = BlogCommentsModel.objects.all()
        tagObj = TagsModel.objects.all()
        extraData["likes"] = len(postLike.filter(blog=pk))
        extraData["comments"] = len(postComments.filter(blog=pk))
        extraData["tags"] = tagObj.filter(blogtagmodel__blog=pk).values_list('tagName', flat=True)
        responseData = blogPostSerializer.data
        responseData.update(extraData)
        return Response(responseData)

    def put(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        realAuthor = request.user.id
        blogPostObj = BlogPostModel.objects.get(pk=pk)
        if realAuthor is not blogPostObj.author_id:
            raise APIException("you are not authorized for this action")
        blogSerializer = BlogPostSerializer(blogPostObj, data=request.data, partial=True)
        if blogSerializer.is_valid():
            blogSerializer.save()
            return Response(data=blogSerializer.data)
        else:
            return Response(blogSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogLikeView(generics.CreateAPIView):
    queryset = BlogLikeModel.objects.all()
    serializer_class = BlogLikeDisLikeSerializer

    def post(self, request, *args, **kwargs):
        request.data["sender"] = request.user.pk
        data = request.data
        like, created = BlogLikeModel.objects.get_or_create(blog_id=data["blog"], sender_id=data["sender"])
        if not created:
            like.delete()
        return Response(data=True)


class BlogCommentCreateView(generics.CreateAPIView):
    queryset = BlogCommentsModel.objects.all()
    serializer_class = BlogCommentSerializer

    def post(self, request, *args, **kwargs):
        request.data["author"] = request.user.pk
        return self.create(request, *args, **kwargs)


class PostCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_class = JWTTokenUserAuthentication
    permission_classes = (IsAuthenticated,)
    queryset = BlogCommentsModel.objects.all()
    serializer_class = BlogCommentSerializer

    def put(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        realAuthor = request.user.id
        comment = BlogCommentsModel.objects.get(pk=pk)
        if realAuthor is not comment.author_id:
            raise APIException("you are not authorized for this action")
        commentSerializer = BlogCommentSerializer(comment, data=request.data, partial=True)
        if commentSerializer.is_valid():
            commentSerializer.save()
            return Response(data=commentSerializer.data)
        else:
            return Response(commentSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllPostComment(generics.ListAPIView):
    authentication_class = JWTTokenUserAuthentication
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogCommentSerializer

    def get_queryset(self):
        return BlogCommentsModel.objects.filter(postId=self.kwargs['pk'])


class GetBlogTags(generics.ListAPIView):
    queryset = BlogTagModel.objects.all()
    serializer_class = BlogTagSerializer
