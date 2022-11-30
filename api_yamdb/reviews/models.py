from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='title'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'