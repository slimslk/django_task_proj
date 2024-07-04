from rest_framework.generics import ListAPIView

from task_app.controllers.v2.base_controller import BaseListCreateGenericView, BaseRetrieveUpdateDeleteGenericView
from task_app.models import Task
from task_app.serializers.task_serializer import TaskDetailSerializer, TaskCreateSerializer, AllTasksSerializer


class TaskListCreateGenericView(BaseListCreateGenericView):
    base_model = Task
    serializer_get = TaskDetailSerializer
    serializer_post = TaskCreateSerializer


class TaskRetrieveUpdateDestroyGenericView(BaseRetrieveUpdateDeleteGenericView):
    base_model = Task
    serializer_get = TaskDetailSerializer
    serializer_put = TaskCreateSerializer


class TaskListByOwnerView(ListAPIView):
    serializer_class = AllTasksSerializer

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)
