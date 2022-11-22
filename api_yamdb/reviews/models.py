from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin')
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    bio = models.TextField(
        'Биография',
        blank=True,
    )



class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField()
    rating = models.IntegerField(blank=True, null=True)
    description = models.TextField("Описание")
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL, related_name="title", null=True
    )
    genre = models.ManyToManyField(Genres, through="GenreTitles")

    def __str__(self):
        return self.name

class Rewiews(models.Model):
    title = models.ForeignKey(
        Titles,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='rewiews',
        verbose_name='отзыв к произведению'
    )
    text = models.TextField(
        'Текст отзыва',
        help_text='Введите текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rewiews',
        verbose_name='автор отзыва'
    )
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
        )
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата отзыва'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

class Comments(models.Model):
    rewiew = models.ForeignKey(
        Rewiews,
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
        Titles,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Наименование",
        related_name="title",
    )
    genre = models.ForeignKey(
        Genres,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Жанр",
        related_name="genre",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["title", "genre"], name="unique_genres")
        ]
