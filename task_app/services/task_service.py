import datetime

from task_app.exceptions.task_app_exception import BadRequestException, NoContentException
from task_app.models import Task
from task_app.serializers.task_serializer import TaskSerializer

from django.utils import timezone


class TaskService:

    def get_all_tasks(self):
        return self.get_tasks()

    def create_new_task(self, task_data: dict):
        serializer = TaskSerializer(data=task_data)
        if not serializer.is_valid(raise_exception=True):
            return serializer.errors

        serializer.save()
        return serializer.data

    def get_task_by_pk(self, task_pk: int):
        return self.get_tasks(pk=task_pk)

    def filter_tasks_by_query_params(self, query_params):
        task_filter = {}
        if status := query_params.get("status"):
            task_filter['status'] = status
        if deadline := query_params.get("deadline"):
            try:
                task_filter['deadline'] = timezone.make_aware(datetime.datetime.strptime(deadline, "%Y-%m-%d"))
            except ValueError:
                message = (f"Incorrect query parameter 'deadline': {deadline}, "
                           f"you should enter the deadline date in YYYY-MM-DD format")
                raise BadRequestException(message)

        return self.get_tasks(**task_filter)

    def get_tasks(self, *args, **kwargs):
        tasks = Task.objects.filter(**kwargs).all()
        if not tasks:
            raise NoContentException()
        if len(tasks) < 2:
            return TaskSerializer(tasks[0]).data

        return TaskSerializer(tasks, many=True).data
