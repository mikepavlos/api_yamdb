import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, permissions, viewsets

from .mixins import ListCreateDestroyViewSet
from .filters import TitlesFilter
from reviews.models import (Category, Genre, Title)
from .serializers import (
    CategorySerializer, 
    GenreSerializer,
    TitleSerializer, 
    TitleWriteSerializer,
)

class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    #Добавить perrmission
    permission_classes = ()


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    #Добавить perrmission
    permission_classes = ()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    #Добавить perrmission
    permission_classes = ()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleWriteSerializer
        return TitleSerializer