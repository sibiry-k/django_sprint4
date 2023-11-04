from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import Http404
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from .models import Post, Category, Comment
from .forms import PostForm, CommentForm

from . import constants


User = get_user_model()


class PostMixin:
    """Mixin for Post."""

    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog:index')


class PostListView(ListView):
    """Display all posts in index page."""

    model = Post
    paginate_by = constants.PAGINATE_PAGE_NUM
    template_name = 'blog/index.html'

    def get_queryset(self):
        return Post.objects.filter(
            pub_date__lt=timezone.now(),
            is_published=True,
            category__is_published=True,
        ).annotate(comment_count=Count('comments')).order_by('-pub_date')


class PostCreateView(LoginRequiredMixin, PostMixin, CreateView):
    """Create post."""

    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user])

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, PostMixin, UpdateView):
    """Edit post."""

    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['post_id'])
        if instance.author != request.user:
            return redirect('blog:post_detail', pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse('blog:profile', args=[self.request.user])
        return reverse('blog:post_detail', pk=self.kwargs.get('post_id'))


class PostDetailView(DetailView):
    """Display unique post."""

    model = Post
    context_object_name = 'post'
    template_name = 'blog/detail.html'

    def get_object(self):
        object = get_object_or_404(Post, pk=self.kwargs['pk'])
        if object.is_published == constants.TTRUE:
            return object
        else:
            if object.author == self.request.user:
                return object
            else:
                raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """Delete post."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object)
        return context


def category_posts(request, slug):
    """Dispaly all post in category."""
    category = get_object_or_404(
        Category,
        slug=slug,
        is_published=True
    )
    posts = category.posts.filter(
        pub_date__lt=timezone.now(),
        is_published=True,
        category__is_published=True,
    ).annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')
    paginator = Paginator(posts, constants.PAGINATE_PAGE_NUM)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'category': category,
    }
    return render(request, 'blog/category.html', context)


class ProfileDetailView(DetailView):
    """Display profile."""

    model = User
    fields = '__all__'
    context_object_name = 'profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'blog/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        paginator = Paginator(posts, constants.PAGINATE_PAGE_NUM)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Edit profile."""

    model = User
    fields = ('username', 'last_name', 'first_name', 'email')
    template_name = 'blog/user.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    success_url = reverse_lazy('login')


@login_required
def add_comment(request, post_id):
    """Function for add comment to post."""
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', pk=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    """Function for edit comment."""
    post = get_object_or_404(Post, pk=post_id)
    instance = get_object_or_404(Comment, pk=comment_id)
    form = CommentForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'post_id': post_id,
        'comment': instance,
    }
    if instance.author == request.user:
        if form.is_valid():
            comment = form.save()
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', pk=post_id)
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, post_id, comment_id):
    """Function delete comment."""
    comment = get_object_or_404(Comment, pk=comment_id)
    context = {
        'comment': comment,
    }
    if request.method == 'POST':
        if comment.author == request.user:
            comment.delete()
            return redirect('blog:post_detail', pk=post_id)
    return render(request, 'blog/comment.html', context)
