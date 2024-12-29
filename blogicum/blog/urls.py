"""URLs of blog app."""
from django.urls import path
from .views import (
    post_detail, create_post, delete_post,
    add_comment, delete_comment,
    edit_profile, ProfileListView,
    IndexView, CategoryListView
)

app_name = 'blog'

urlpatterns = [
    path(
        '',
        IndexView.as_view(),
        name='index'
    ),
    path(
        'category/<slug:category_slug>/',
        CategoryListView.as_view(),
        name='category_posts'
    ),
    path(
        'profile/<str:username>/',
        ProfileListView.as_view(),
        name='profile'
    ),
    path(
        'profile/edit',
        edit_profile,
        name='edit_profile'
    ),
    path(
        'posts/<int:post_id>/',
        post_detail,
        name='post_detail'
    ),
    path(
        'posts/create/',
        create_post,
        name='create_post'
    ),
    path(
        'posts/<int:pk_post>/edit/',
        create_post,
        name='edit_post'
    ),
    path(
        'posts/<int:pk_post>/delete/',
        delete_post,
        name='delete_post'
    ),
    path(
        'posts/<int:post_id>/comment/',
        add_comment,
        name='add_comment'
    ),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        add_comment,
        name='edit_comment'
    ),
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        delete_comment,
        name='delete_comment'
    )
]
