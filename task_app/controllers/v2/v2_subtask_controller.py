from task_app.controllers.v2.base_controller import BaseListCreateGenericView, BaseRetrieveUpdateDeleteGenericView
from task_app.models import Subtask
from task_app.serializers.subtask_serializer import SubtaskDetailSerializer, SubtaskCreateSerializer


class SubtaskListCreateGenericView(BaseListCreateGenericView):
    base_model = Subtask
    serializer_get = SubtaskDetailSerializer
    serializer_post = SubtaskCreateSerializer


class SubtaskRetrieveUpdateDestroyGenericView(BaseRetrieveUpdateDeleteGenericView):
    base_model = Subtask
    serializer_get = SubtaskDetailSerializer
    serializer_put = SubtaskCreateSerializer
