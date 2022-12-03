from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    UserViewSet,
    SignUpView,
    GetTokenView)

router_v1 = DefaultRouter()

router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(r'titles', TitleViewSet)
router_v1.register(r'users', UserViewSet,)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', GetTokenView.as_view(), name='token'),
]
