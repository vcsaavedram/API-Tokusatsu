from rest_framework import serializers
from .models import Franchise, Series

class FranchiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Franchise
        fields = [
            'id',
            'name',
            'production_company',
            'creation_year'
        ]

class SeriesSerializer(serializers.ModelSerializer):
    franchise_name = serializers.CharField(source='franchise.name', read_only=True)
    base_series_title = serializers.CharField(source='base_series.title', read_only=True)

    class Meta:
        model = Series
        fields = [
            'id',
            'franchise',
            'franchise_name',
            'base_series',
            'base_series_title',
            'title',
            'platform', 
            'release_year', 
            'episode_count', 
            'theme', 
            'is_airing'
        ]