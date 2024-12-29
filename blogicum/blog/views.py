"""Views of blog app."""
from django.shortcuts import render, redirect
from django.http import Http404
from django.db.models import Q
from django.utils import timezone
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from .models import Post, Category, Comment, User
from .forms import PostForm, CommentForm, ProfileEditForm


class IndexView(ListView):
    template_name = 'blog/index.html'
    paginate_by = 10

    def get_queryset(self):
        page_obj = Post.objects.filter(
            Q(is_published=True)
            & Q(pub_date__lte=timezone.now())
            & Q(category__is_published=True)
        ).order_by(
            "-pub_date"
        ).annotate(comment_count=Count("comment"))
        return page_obj

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class CategoryListView(ListView):
    template_name = 'blog/category.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        Cat = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug']
        )
        page_obj = Cat.post.filter(
            is_published=True,
            pub_date__lte=timezone.now()
        ).order_by(
            "-pub_date"
        ).annotate(comment_count=Count("comment"))
        return page_obj

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        slug = self.kwargs['category_slug']
        Cat = get_object_or_404(
            Category,
            slug=slug
        )
        context['category'] = Cat
        if not Cat.is_published:
            raise Http404(f"Category with slug = {slug} does not exist")
        return context


class ProfileListView(ListView):
    template_name = 'blog/profile.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        profile = get_object_or_404(
            User,
            username=self.kwargs['username'],
        )
        page_obj = Post.objects.filter(
            author=profile
        ).order_by(
            "-pub_date"
        ).annotate(
            comment_count=Count("comment")
        )
        return page_obj

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        username = self.kwargs['username']
        profile = get_object_or_404(
            User,
            username=username,
        )
        context['profile'] = profile
        return context


@login_required(login_url='/auth/login/')
def edit_profile(request):
    """Profile view."""
    profile = request.user
    form = ProfileEditForm(
        request.POST,
        instance=profile
    )
    context = {
        'profile': profile,
        'form': form,
    }
    if form.is_valid():
        new_info = form.save(commit=False)
        profile.first_name = new_info.first_name
        profile.last_name = new_info.last_name
        profile.email = new_info.email
        profile.username = new_info.username
        profile.save()
        return redirect('blog:profile', profile.username)

    return render(request, 'blog/user.html', context)


def post_detail(request, post_id):
    """Render index detail view."""
    cur = get_object_or_404(
        Post,
        pk=post_id,
    )
    if request.user != cur.author:
        cur = get_object_or_404(
            Post,
            pk=post_id,
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        )

    comments = Comment.objects.filter(
        post=cur
    )
    form = CommentForm()
    context = {
        "post": cur,
        "form": form,
        "comments": comments,
    }
    return render(request, 'blog/detail.html', context)


@login_required(login_url='/auth/login/')
def create_post(request, pk_post=None):
    """Post creation/edit view."""
    user = request.user

    if pk_post is None:
        instance = None
    else:
        instance = get_object_or_404(Post, id=pk_post)
        if user != instance.author:
            return redirect('blog:post_detail', instance.pk)

    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=instance
    )
    context = {'form': form}

    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        return redirect('blog:profile', user.username)

    return render(request, 'blog/create.html', context)


@login_required(login_url='/auth/login/')
def delete_post(request, pk_post):
    """Post deletion view."""
    user = request.user
    instance = get_object_or_404(
        Post,
        pk=pk_post
    )

    if user != instance.author and not user.is_staff:
        return redirect('blog:post_detail', instance.pk)

    form = PostForm(instance=instance)
    context = {'form': form}

    if request.method == 'POST':
        instance.delete()
        return redirect('blog:index')

    return render(request, 'blog/create.html', context)


@login_required(login_url='/auth/login/')
def add_comment(request, post_id, comment_id=None):
    """Comment creation"""
    user = request.user

    if comment_id is None:
        comment = None
    else:
        comment = get_object_or_404(
            Comment,
            pk=comment_id
        )
        if (user != comment.author):
            return redirect('blog:post_detail', post_id)

    post = get_object_or_404(
        Post,
        pk=post_id,
    )

    form = CommentForm(
        request.POST or None,
        instance=comment
    )
    context = {
        'form': form,
        'comment': comment
    }

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = user
        comment.post = post
        comment.save()
        return redirect('blog:post_detail', post.pk)

    return render(request, 'blog/comment.html', context)


@login_required(login_url='/auth/login/')
def delete_comment(request, post_id, comment_id):
    user = request.user
    comment = get_object_or_404(
        Comment,
        pk=comment_id
    )

    if (user != comment.author):
        return redirect('blog:post_detail', post_id)

    context = {
        'comment': comment
    }

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id)

    return render(request, 'blog/comment.html', context)
