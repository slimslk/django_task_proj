from task_app.controllers.v2.base_controller import BaseListCreateGenericView, BaseRetrieveUpdateDeleteGenericView
from task_app.models import Task
from task_app.serializers.task_serializer import TaskDetailSerializer, TaskCreateSerializer


class TaskListCreateGenericView(BaseListCreateGenericView):
    base_model = Task
    serializer_get = TaskDetailSerializer
    serializer_post = TaskCreateSerializer


class TaskRetrieveUpdateDestroyGenericView(BaseRetrieveUpdateDeleteGenericView):
    base_model = Task
    serializer_get = TaskDetailSerializer
    serializer_put = TaskCreateSerializer
