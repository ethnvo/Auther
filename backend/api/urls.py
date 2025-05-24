# backend/api/urls.py

from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    SearchPapersView,
    FavoriteViewSet,
    RecentlyViewedViewSet,
)

router = DefaultRouter()
router.register('favorites', FavoriteViewSet, basename='favorite')
router.register('recently-viewed', RecentlyViewedViewSet, basename='recently-viewed')

urlpatterns = [
    path('papers/', SearchPapersView.as_view(), name='paper-search'),
]

urlpatterns += router.urls
