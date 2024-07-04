from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from task_app.controllers.v1.statistic_controller import StatisticListApiView
from task_app.controllers.v1.task_controller import (
    TaskListAPIView,
    TaskDetailAPIView
)
from task_app.controllers.v1.subtask_controller import (
    SubtaskListApiView,
    SubtaskDetailApiView
)

urlpatterns = [
    path('tasks/', TaskListAPIView.as_view()),
    path('tasks/<int:task_pk>/', TaskDetailAPIView.as_view()),
    path('statistic/', StatisticListApiView.as_view()),
    path('subtasks/', SubtaskListApiView.as_view()),
    path('subtasks/<int:subtask_id>/', SubtaskDetailApiView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
