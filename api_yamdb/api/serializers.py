from rest_framework import serializers
from reviews.models import (Category, Comment, Genre, Review, Title, User)
from django.db.models import Avg
from rest_framework.validators import UniqueTogetherValidator


class CategorySerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Category
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Genre
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), 
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), 
        slug_field='slug', 
        many=True,
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
        'description', 'genre', 'category'
        )
        read_only_fields = (
            'id', 'rating'
        )
    
    def get_rating(self, obj):
        rating = obj.avg
        if rating == None:
            return "None"
        return round(rating)


class GetTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        return value


class MeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
        read_only_fields = ('role',)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = (
            'id', 'text', 'author', 'score', 'pub_date'
        )
        read_only_fields = ('id')
        model = Review


    def validate_score(self,score):
        if score != int:
            raise serializers.ValidationError('Оценка должна быть целым числом')
        if 1 > score > 10:
            raise serializers.ValidationError('Оценка должна быть от 1 до 10')
        return score


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = (
            'id', 'text', 'author', 'pub_date'
        )
        read_only_fields = ('id')
        model = Comment
