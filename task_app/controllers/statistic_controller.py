from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from task_app.exceptions.task_app_exception import TaskAppBaseException
from task_app.services.statistic_service import StatisticService


class StatisticListApiView(APIView):

    service = StatisticService()

    def get(self, request: Request) -> Response:
        try:
            statistic = self.service.get_task_statistic()
        except TaskAppBaseException as err:
            return Response(err.data, status=err.status_code)

        return Response(data=statistic, status=status.HTTP_200_OK)
