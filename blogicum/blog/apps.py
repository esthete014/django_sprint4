"""Blog apps."""
from django.apps import AppConfig


class BlogConfig(AppConfig):
    """BlogConfig apps."""

    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = 'Блог'
    name = 'blog'
