from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SearchPapersView, FavoriteViewSet, RecentlyViewedViewSet

router = DefaultRouter()
router.register("favorites", FavoriteViewSet, basename="favorite")
router.register("recently-viewed", RecentlyViewedViewSet, basename="recently-viewed")

urlpatterns = [
    path("papers/", SearchPapersView.as_view(), name="paper-search"),
    path("", include(router.urls)),
]
