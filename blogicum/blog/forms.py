from django import forms
from . import views


class PostForm(forms.ModelForm):

    class Meta():
        model = views.Post
        exclude = [
            'author',
            'is_published'
        ]


class CommentForm(forms.ModelForm):

    class Meta():
        model = views.Comment
        fields = ('text',)


class ProfileEditForm(forms.ModelForm):

    class Meta():
        model = views.User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
        )
