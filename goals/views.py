from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from goals.permissions import UserAuthenticated
from goals.serializers import comments_serializers
from goals.serializers.goals_serializers import GoalCreateSerializer, GoalListSerializers, GoalsRUDSerializers
from goals.serializers.category_serializers import GoalCategorySerializers, GoalCategorySerializer
from goals.models import GoalCategory, Goals, GoalComment
from goals.filters import GoalDateFilter


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializers
    permission_classes = [IsAuthenticated, UserAuthenticated]


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [IsAuthenticated]
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
        return GoalCategory.objects.filter(
            user=self.request.user, is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [IsAuthenticated, UserAuthenticated]

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


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


class GoalCommentsCreateView(CreateAPIView):
    model = GoalComment
    serializer_class = comments_serializers.CommentsCreateSerializers
    permission_classes = [IsAuthenticated, UserAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GoalCommentsListView(ListAPIView):
    model = GoalComment
    permission_classes = [IsAuthenticated, UserAuthenticated]
    serializer_class = comments_serializers.GoalCommentsListSerializers
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    filterset_fields = ['goal']
    ordering = ['created']

    def get_queryset(self):
        return GoalComment.objects.filter(user=self.request.user)


class CommentsRUDView(RetrieveUpdateDestroyAPIView):
    queryset = GoalComment.objects.all()
    serializer_class = comments_serializers.CommentsRUDSerializers
    permission_classes = [IsAuthenticated, UserAuthenticated]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
