from django.contrib.auth import get_user_model
from django.db import models

from . import constants

User = get_user_model()


class PublishedCreatedModel(models.Model):
    """Describes the abstract Base model."""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )

    class Meta:
        abstract = True


class Category(PublishedCreatedModel):
    """Describes the Category model."""

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, '
                   'цифры, дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:constants.TRUNCSTR_TITLE]


class Location(PublishedCreatedModel):
    """Describes the Location model."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название места',
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:constants.TRUNCSTR_TITLE]


class Post(PublishedCreatedModel):
    """Describes the Post model."""

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем — '
                   'можно делать отложенные публикации.')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
        related_name='posts',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts',
    )
    image = models.ImageField('Фото', blank=True)

    class Meta:
        ordering = ('-pub_date',)
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title[:constants.TRUNCSTR_TITLE]


class Comment(models.Model):
    text = models.TextField('Текст комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)
