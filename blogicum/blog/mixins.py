from django.contrib.auth import get_user_model
from django.db.models import Count
from django.urls import reverse_lazy
from django.utils import timezone

from .models import Post
from .forms import PostForm

User = get_user_model()


class PostMixin:
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog:index')


class PostGetQuerySetMixin:
    def get_queryset_posts(self):
        return Post.objects.filter(
            pub_date__lt=timezone.now(),
            is_published=True,
            category__is_published=True,
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')


class ProfileGetPostsMixin:
    def get_posts(self):
        if self.object != self.request.user:
            posts = Post.objects.filter(
                author_id=self.object.id,
                pub_date__lt=timezone.now(),
                is_published=True,
                category__is_published=True,
            ).order_by(
                '-pub_date'
            ).annotate(
                comment_count=Count('comments')
            )
        else:
            posts = Post.objects.filter(
                author_id=self.object.id
            ).order_by(
                '-pub_date'
            ).annotate(
                comment_count=Count('comments')
            )
        return posts
