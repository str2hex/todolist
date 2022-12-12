from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from ..filters import GoalDateFilter
from ..models.goals import Goals
from ..permissions import UserAuthenticated
from ..serializers.goals_serializers import GoalCreateSerializer, GoalListSerializers, GoalsRUDSerializers


class GoalCreateView(CreateAPIView):
    model = Goals
    permission_classes = [IsAuthenticated, UserAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    model = Goals
    permission_classes = [IsAuthenticated]
    serializer_class = GoalListSerializers
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ["priority", "due_date"]
    ordering = ["priority", "due_date"]
    search_fields = ["title"]

    def get_queryset(self):
        return Goals.objects.filter(user=self.request.user).exclude(status=Goals.Status.archived)


class GoalRUDlView(RetrieveUpdateDestroyAPIView):
    queryset = Goals.objects.all()
    serializer_class = GoalsRUDSerializers
    permission_classes = [IsAuthenticated, UserAuthenticated]

    def perform_destroy(self, instance):
        instance.status = Goals.Status.archived
        instance.save()
        return instance
