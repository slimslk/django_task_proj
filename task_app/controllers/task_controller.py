from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from task_app.exceptions.task_app_exception import TaskAppBaseException
from task_app.services.task_service import TaskService


class TaskListAPIView(APIView):

    service = TaskService()

    def get(self, request: Request, *args, **kwargs) -> Response:
        try:
            if request.query_params:
                tasks = self.service.filter_tasks_by_query_params(request.query_params)
            else:
                tasks = self.service.get_all_tasks()
        except TaskAppBaseException as err:
            return Response(err.data, status=err.status_code)

        return Response(data=tasks, status=status.HTTP_200_OK)

    def post(self,  request: Request, *args, **kwargs) -> Response:
        data = self.service.create_new_task(
            request.data
        )

        return Response(data=data, status=status.HTTP_201_CREATED)


class TaskDetailAPIView(APIView):

    service = TaskService()

    def get(self, request: Request, *args, **kwargs) -> Response:
        try:
            task = self.service.get_task_by_pk(kwargs.get("task_pk"))
        except TaskAppBaseException as err:
            return Response(err.data, status=err.status_code)
        return Response(task, status=status.HTTP_200_OK)
