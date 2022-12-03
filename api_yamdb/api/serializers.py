from rest_framework import serializers
from reviews.models import (Category, Genre, Title, User)


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

    class Meta:
        model = Title
        fields = '__all__'


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


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    confirmation_code = serializers.CharField(required=True)
