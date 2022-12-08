from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import username_validator, year_validator

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

ROLE_CHOICES = (
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
    (USER, USER),
)

ROLE_MAX_LENGTH = max(len(i[0]) for i in ROLE_CHOICES)


class User(AbstractUser):
    username = models.CharField(
        unique=True,
        max_length=150,
        validators=[username_validator]
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
    )
    bio = models.TextField(
        blank=True,
    )
    role = models.CharField(
        max_length=ROLE_MAX_LENGTH,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR


class CommonCategoryGenre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(CommonCategoryGenre):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CommonCategoryGenre):

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField(validators=[year_validator])
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        through='TitleGenre'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        unique_together = ('author', 'title')

    def __str__(self):
        return str(self.pk)


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
