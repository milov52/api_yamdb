from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin')
    )

    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default='user'
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField()
    description = models.TextField("Описание")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="title", null=True
    )
    genre = models.ManyToManyField(Genre, through="GenreTitles")

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='отзыв к произведению'
    )
    text = models.TextField(
        'Текст отзыва',
        help_text='Введите текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор отзыва'
    )
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата отзыва'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique review')
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='комментарий к отзыву'
    )
    text = models.TextField(
        'текст комментария',
        help_text='введите текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор комментария'
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='дата комментария'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class GenreTitles(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Наименование",
        related_name="title",
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Жанр",
        related_name="genre",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "genre"], name="unique_genres"
            )
        ]
