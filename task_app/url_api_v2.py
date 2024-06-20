from django.urls import path, include
from rest_framework.routers import DefaultRouter

from task_app.controllers.v2.v2_categories_controller import CategoryViewSet
from task_app.controllers.v2.v2_subtask_controller import (
    SubtaskListCreateGenericView,
    SubtaskRetrieveUpdateDestroyGenericView
)
from task_app.controllers.v2.v2_task_controller import (
    TaskListCreateGenericView,
    TaskRetrieveUpdateDestroyGenericView
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('tasks/', TaskListCreateGenericView.as_view()),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyGenericView.as_view()),
    path('subtasks/', SubtaskListCreateGenericView.as_view()),
    path('subtasks/<int:pk>/', SubtaskRetrieveUpdateDestroyGenericView.as_view()),
    path('', include(router.urls))
]
