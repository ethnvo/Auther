from django.urls import path
from .views import PaperListView

urlpatterns = [
    path('papers/', PaperListView.as_view(), name='paper-list'),
]
