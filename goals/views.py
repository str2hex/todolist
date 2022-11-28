from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

from . import models, serializers
from .serializers import GoalCategorySerializer


class GoalCategoryCreateView(CreateAPIView):
    model = models.GoalCategory
    serializer_class = serializers.GoalCategorySerializers
    permission_classes = [permissions.IsAuthenticated]


class LimitOffsetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10000


class GoalCategoryListView(ListAPIView):
    model = models.GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return models.GoalCategory.objects.filter(
            user=self.request.user, is_deleted=False
        )
