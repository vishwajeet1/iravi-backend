from django.urls import path

from .views import BlogListCreateView, BlogLikeView, BlogCommentCreateView, \
    PostCommentDetailView, GetAllPostComment, BlogPostDetailView, GetBlogTags

urlpatterns = [
    path('blog', BlogListCreateView.as_view()),
    path('blog/<int:pk>', BlogPostDetailView.as_view()),
    path('blog/like', BlogLikeView.as_view()),
    path('blog/comment', BlogCommentCreateView.as_view()),
    path('blog/comment/<int:pk>', PostCommentDetailView.as_view()),
    path('blog/post/<int:pk>/comment', GetAllPostComment.as_view()),
    path('tag', GetBlogTags.as_view())
]
