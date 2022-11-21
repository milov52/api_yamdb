from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField()
    rating = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name="title",
        null=True
    )

    def __str__(self):
        return self.name


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
