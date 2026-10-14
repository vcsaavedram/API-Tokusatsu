from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FranchiseViewSet, SeriesViewSet

router = DefaultRouter()
router.register(r'franchises', FranchiseViewSet)
router.register(r'series', SeriesViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]