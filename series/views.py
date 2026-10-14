from rest_framework import viewsets, permissions
from .models import Franchise, Series
from .serializers import FranchiseSerializer, SeriesSerializer

class FranchiseViewSet(viewsets.ModelViewSet):
    queryset = Franchise.objects.all().order_by('creation_year')
    serializer_class = FranchiseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all().order_by('-release_year')
    serializer_class = SeriesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]