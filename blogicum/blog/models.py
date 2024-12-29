from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class AbstractFieldsModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    created_at = models.DateTimeField(
        auto_created=True,
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta():
        abstract = True


class Category(AbstractFieldsModel):
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL;'
                   + ' разрешены символы латиницы,'
                   + ' цифры, дефис и подчёркивание.')
    )

    class Meta():
        verbose_name = 'категория'
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Location(AbstractFieldsModel):
    name = models.CharField(
        max_length=256,
        verbose_name='Название места'
    )

    class Meta():
        verbose_name = 'местоположение'
        verbose_name_plural = "Местоположения"

    def __str__(self):
        return self.name


class Post(AbstractFieldsModel):
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
    )
    image = models.ImageField(
        upload_to="media/",
        null=True,
        blank=True,
        verbose_name='Изображение'
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем'
                   + ' — можно делать отложенные публикации.')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='post',
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='post',
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='post',
        verbose_name='Категория'
    )

    class Meta():
        verbose_name = 'публикация'
        verbose_name_plural = "Публикации"
        ordering = ["-pub_date"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(
        verbose_name='Текст'
    )
    created_at = models.DateTimeField(
        auto_created=True,
        auto_now_add=True,
        verbose_name='Добавлено'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comment',
        verbose_name='Публикация'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment',
        verbose_name='Автор публикации'
    )

    class Meta():
        verbose_name = 'коментарий'
        verbose_name_plural = "Коментарии"
        ordering = ('created_at',)
