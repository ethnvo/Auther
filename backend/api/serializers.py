from rest_framework import serializers
from .models import Paper, Favorite, RecentlyViewed

class PaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paper
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    paper = PaperSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'paper', 'created_at']

class RecentlyViewedSerializer(serializers.ModelSerializer):
    # Show full paper detail on GET
    paper = PaperSerializer(read_only=True)
    # Accept paper_id on POST
    paper_id = serializers.PrimaryKeyRelatedField(
        queryset=Paper.objects.all(),
        write_only=True,
        source='paper'
    )

    class Meta:
        model = RecentlyViewed
        fields = ['id', 'paper', 'paper_id', 'viewed_at']
