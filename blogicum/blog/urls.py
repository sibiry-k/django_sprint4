from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(),
         name='index'),
    path('posts/create/', views.PostCreateView.as_view(),
         name='create_post'),
    path('posts/<int:post_id>/edit/', views.PostUpdateView.as_view(),
         name='edit_post'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(),
         name='delete_post'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(),
         name='post_detail'),
    path('category/<slug:slug>/', views.category_posts,
         name='category_posts'),
    path('profile/<slug:username>/edit/', views.ProfileUpdateView.as_view(),
         name='edit_profile'),
    path('profile/<slug:username>/', views.ProfileDetailView.as_view(),
         name='profile'),
    path('posts/<int:post_id>/comment/', views.add_comment,
         name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
         views.edit_comment, name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         views.delete_comment, name='delete_comment'),

]
