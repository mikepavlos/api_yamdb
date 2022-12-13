from django.conf import settings
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import year_validator, username_validator


class CommonCategoryGenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        lookup_field = 'slug'


class CategorySerializer(CommonCategoryGenreSerializer):

    class Meta(CommonCategoryGenreSerializer.Meta):
        model = Category


class GenreSerializer(CommonCategoryGenreSerializer):

    class Meta(CommonCategoryGenreSerializer.Meta):
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        read_only_fields = fields


class TitleWriteSializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        read_only_fields = ('id', 'rating')

    def get_rating(self, obj):
        queryset_avg = Title.objects.annotate(rating=Avg('reviews__score'))
        title = queryset_avg.get(pk=obj.pk)
        if title.rating is None:
            return None
        return round(title.rating)

    def validate_year(self, value):
        return year_validator(value)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    score = serializers.IntegerField(
        min_value=settings.MIN_SCORE,
        max_value=settings.MAX_SCORE
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id',)

    def validate(self, data):
        request = self.context['request']
        if request.method != 'POST':
            return data
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if Review.objects.filter(
                author=request.user,
                title=title
        ).exists():
            raise serializers.ValidationError(
                'Отзыв на это произведение уже написан.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id',)


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.USERNAME_LENGTH,
        required=True,
        validators=[username_validator]
    )
    email = serializers.EmailField(
        max_length=settings.EMAIL_LENGTH,
        required=True
    )

    class Meta:
        fields = ('email', 'username')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=settings.USERNAME_LENGTH,
        validators=[username_validator])
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, value):
        return username_validator(value)


class MeSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)
