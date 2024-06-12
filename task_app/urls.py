from django.urls import path

from task_app.controllers.statistic_controller import StatisticListApiView
from task_app.controllers.task_controller import TaskListAPIView, TaskDetailAPIView

urlpatterns = [
    path('tasks/', TaskListAPIView.as_view()),
    path('tasks/<int:task_pk>', TaskDetailAPIView.as_view()),
    path('statistic/', StatisticListApiView.as_view())
]
