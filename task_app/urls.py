from django.urls import path

from task_app.controllers.statistic_controller import StatisticListApiView
from task_app.controllers.task_controller import (
    TaskListAPIView,
    TaskDetailAPIView
)
from task_app.controllers.subtask_controller import (
    SubtaskListApiView,
    SubtaskDetailApiView
)

urlpatterns = [
    path('tasks/', TaskListAPIView.as_view()),
    path('tasks/<int:task_pk>/', TaskDetailAPIView.as_view()),
    path('statistic/', StatisticListApiView.as_view()),
    path('subtasks/', SubtaskListApiView.as_view()),
    path('subtasks/<int:subtask_id>/', SubtaskDetailApiView.as_view())
]
