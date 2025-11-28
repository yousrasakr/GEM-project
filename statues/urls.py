from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StatueViewSet

router = DefaultRouter()
router.register(r'statues', StatueViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
