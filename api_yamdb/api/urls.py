from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

router_v1 = DefaultRouter()

router_v1.register(r'users', UserViewSet,)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
