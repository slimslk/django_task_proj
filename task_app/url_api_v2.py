from django.urls import path

from task_app.controllers.v2.v2_subtask_controller import (
    SubtaskListCreateGenericView,
    SubtaskRetrieveUpdateDestroyGenericView
)
from task_app.controllers.v2.v2_task_controller import (
    TaskListCreateGenericView,
    TaskRetrieveUpdateDestroyGenericView
)

urlpatterns = [
    path('tasks/', TaskListCreateGenericView.as_view()),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyGenericView.as_view()),
    path('subtasks/', SubtaskListCreateGenericView.as_view()),
    path('subtasks/<int:pk>/', SubtaskRetrieveUpdateDestroyGenericView.as_view()),
]
