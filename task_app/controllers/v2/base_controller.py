from abc import ABC

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from task_app.models import Subtask, Task
from task_app.permissions.owner_permission import IsOwnerOrAuthenticatedReadOnly
from task_app.serializers.subtask_serializer import SubtaskDetailSerializer, SubtaskCreateSerializer
from task_app.serializers.task_serializer import TaskDetailSerializer, TaskCreateSerializer


class AppPageNumberPaginator(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 5


class BaseListCreateGenericView(ListCreateAPIView):
    base_model: Task | Subtask = None
    serializer_get: TaskDetailSerializer | SubtaskDetailSerializer = None
    serializer_post: TaskCreateSerializer | SubtaskCreateSerializer = None
    permission_classes = [IsAuthenticatedOrReadOnly]

    pagination_class = AppPageNumberPaginator
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_queryset(self):
        assert self.base_model is not None, (
                "'%s' should include a `base_model` attribute."
                % self.__class__.__name__
        )
        return self.base_model.objects.all()

    def get_serializer_class(self):
        assert self.serializer_get is not None, (
            f"'{self.__class__.__name__}' should include a "
            f"`serializer_get` attribute."
        )
        assert self.serializer_post is not None, (
            f"'{self.__class__.__name__}' should include a "
            f"`serializer_post` attribute."
        )
        if self.request.method == 'GET':
            return self.serializer_get

        else:
            return self.serializer_post

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BaseRetrieveUpdateDeleteGenericView(RetrieveUpdateDestroyAPIView):
    base_model: Task | Subtask = None
    serializer_get: TaskDetailSerializer | SubtaskDetailSerializer = None
    serializer_put: TaskCreateSerializer | SubtaskCreateSerializer = None
    permission_classes = [IsOwnerOrAuthenticatedReadOnly]

    def get_object(self):
        assert self.base_model is not None, (
                "'%s' should include a `base_model` attribute."
                % self.__class__.__name__
        )
        obj = get_object_or_404(self.base_model, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_class(self):
        assert self.serializer_get is not None, (
            f"'{self.__class__.__name__}' should include a "
            f"`serializer_get` attribute."
        )
        assert self.serializer_put is not None, (
            f"'{self.__class__.__name__}' should include a "
            f"`serializer_post` attribute."
        )
        if self.request.method in ['PUT', 'PATCH']:
            return self.serializer_put
        else:
            return self.serializer_get
