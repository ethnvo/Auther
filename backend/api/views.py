from rest_framework import generics, filters
from .models import Paper
from .serializers import PaperSerializer
from django.db.models import Q

class PaperListView(generics.ListAPIView):
    serializer_class = PaperSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'abstract', 'authors']  # ✅ search across all 3 fields

    def get_queryset(self):
        queryset = Paper.objects.filter(gender_inference_possible=True)

        if self.request.query_params.get('only_women') == "true":
            queryset = queryset.filter(has_woman_author=True)

        year = self.request.query_params.get('year')
        if year:
            queryset = queryset.filter(date__year=year)

        return queryset.order_by('-has_woman_author', '-id')