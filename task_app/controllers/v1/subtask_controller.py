from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from task_app.exceptions.task_app_exception import TaskAppBaseException
from task_app.repositories.subtask_repository import SubtaskRepository
from task_app.services.subtask_service import SubtaskService


class SubtaskListApiView(APIView):
    def __init__(self, **kwargs):
        subtask_repository = SubtaskRepository()
        self.__service = SubtaskService(subtask_repository=subtask_repository)
        super().__init__(**kwargs)

    def get(self, request: Request) -> Response:
        try:
            subtasks = self.__service.get_all_subtask()
            return Response(data=subtasks, status=status.HTTP_200_OK)

        except TaskAppBaseException as err:
            return Response(err.data, status=err.status_code)

    def post(self, request: Request) -> Response:
        try:
            request_data = request.data
            response = self.__service.create_new_task(request_data)
            return Response(data=response, status=status.HTTP_201_CREATED)

        except TaskAppBaseException as err:
            return Response(err.data, status=err.status_code)


class SubtaskDetailApiView(APIView):
    __subtask_repository = SubtaskRepository()
    __service = SubtaskService(__subtask_repository)

    def get(self, request: Request, subtask_id: int) -> Response:
        try:
            subtask = self.__service.get_subtask_by_id(subtask_id)
            return Response(data=subtask, status=status.HTTP_200_OK)

        except TaskAppBaseException as err:
            return Response(err.data, status=err.status_code)

    def put(self, request: Request, subtask_id: int) -> Response:
        try:
            data = request.data
            response = self.__service.update_subtask(data, subtask_id)
            return Response(data=response, status=status.HTTP_200_OK)

        except TaskAppBaseException as err:
            return Response(err.data, status=err.status_code)

    def delete(self, request: Request, subtask_id: int) -> Response:
        try:
            response = self.__service.delete(subtask_id)
            return Response(data=response, status=status.HTTP_200_OK)

        except TaskAppBaseException as err:
            return Response(err.data, status=err.status_code)
