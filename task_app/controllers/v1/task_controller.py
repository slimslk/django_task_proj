from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from task_app.exceptions.task_app_exception import TaskAppBaseException
from task_app.repositories.category_repository import CategoryRepository
from task_app.repositories.task_repository import TaskRepository
from task_app.services.category_service import CategoryService
from task_app.services.task_service import TaskService


class TaskListAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def __init__(self, **kwargs):
        task_repository = TaskRepository()
        category_repository = CategoryRepository()
        category_service = CategoryService(category_repository=category_repository)
        self.__service = TaskService(task_repository=task_repository, category_service=category_service)
        super().__init__(**kwargs)

    def get(self, request: Request, *args, **kwargs) -> Response:
        try:
            if request.query_params:
                tasks = self.__service.filter_tasks_by_query_params(request.query_params)
            else:
                tasks = self.__service.get_all_tasks()
        except TaskAppBaseException as err:
            return Response(err.data, status=err.status_code)

        return Response(data=tasks, status=status.HTTP_200_OK)

    def post(self,  request: Request, *args, **kwargs) -> Response:
        try:
            data = self.__service.create_new_task(
                request.data
            )
        except TaskAppBaseException as err:
            return Response(err.data, status=err.status_code)

        return Response(data=data, status=status.HTTP_201_CREATED)


class TaskDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        task_repository = TaskRepository()
        category_repository = CategoryRepository()
        category_service = CategoryService(category_repository=category_repository)
        self.__service = TaskService(task_repository=task_repository, category_service=category_service)
        super().__init__(**kwargs)

    def get(self, request: Request, *args, **kwargs) -> Response:
        try:
            task = self.__service.get_task_by_pk(kwargs.get("task_pk"))
        except TaskAppBaseException as err:
            return Response(err.data, status=err.status_code)
        return Response(task, status=status.HTTP_200_OK)
