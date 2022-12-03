import django_filters
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .mixins import ListCreateDestroyViewSet
from .filters import TitlesFilter
from reviews.models import (Category, Genre, Title, User)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    GetTitleSerializer,
    UserSerializer,
    MeSerializer,
    ReviewSerializer
)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    # Добавить perrmission
    permission_classes = ()


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    # Добавить perrmission
    permission_classes = ()


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    # Добавить perrmission
    permission_classes = ()

    def get_queryset(self):
        new_queryset = Title.objects.annotate(avg=Avg('review__score'))
        return new_queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetTitleSerializer
        return TitleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['get', 'patch'],
        detail=True,
        permission_classes=AllowAny
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
        else:
            serializer = MeSerializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = []

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        new_queryset = title.review
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(
            author=self.request.user,
            title_id=title.pk
        )
