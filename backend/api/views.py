# api/views.py

from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, viewsets, mixins

from .models import Paper, Favorite, RecentlyViewed
from .serializers import (
    PaperSerializer,
    FavoriteSerializer,
    RecentlyViewedSerializer,
)
from .scripts.load_papers import fetch_and_filter


class RecentlyViewedViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    POST to record a click, GET to list recent clicks.
    """
    serializer_class = RecentlyViewedSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RecentlyViewed.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SearchPapersView(APIView):
    """
    Cache-backed search endpoint. Does not write to the DB.
    """
    permission_classes = []  # or [permissions.AllowAny]

    def get(self, request):
        q = request.query_params.get("search", "").strip() or "machine learning"
        only_women = request.query_params.get("only_women") == "true"
        year = request.query_params.get("year", "")

        cache_key = f"search:{q}:{only_women}:{year}"
        papers = cache.get(cache_key)
        if papers is None:
            papers = fetch_and_filter(q, only_women, year)
            cache.set(cache_key, papers, timeout=3600)
        return Response(papers)


class FavoriteViewSet(viewsets.ModelViewSet):
    """
    CRUD for user favorites.
    """
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        paper = Paper.objects.get(id=self.request.data["paper_id"])
        serializer.save(user=self.request.user, paper=paper)
