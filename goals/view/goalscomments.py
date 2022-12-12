from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from goals.models.goalscommets import GoalComment
from goals.permissions import UserAuthenticated
from goals.serializers import comments_serializers


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
