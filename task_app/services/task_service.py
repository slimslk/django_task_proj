import datetime

from django.core.paginator import Paginator, InvalidPage

from task_app.exceptions.task_app_exception import BadRequestException, NoContentException, CreateValidationError
from task_app.models import Task
from task_app.serializers.task_serializer import TaskDetailSerializer, TaskCreateSerializer

from django.utils import timezone


class TaskService:
    __PAGE_SIZE = 2

    def get_all_tasks(self):
        return self.get_tasks()

    def create_new_task(self, task_data: dict):
        serializer = TaskCreateSerializer(data=task_data)
        if not serializer.is_valid(raise_exception=True):
            raise CreateValidationError(serializer.errors)

        serializer.save()
        return serializer.data

    def get_task_by_pk(self, task_pk: int):
        return self.get_tasks(pk=task_pk)

    def filter_tasks_by_query_params(self, query_params):
        task_filter = {}
        is_error = False
        message = {}
        if status := query_params.get("status"):
            task_filter['status'] = status

        if deadline := query_params.get("deadline"):
            try:
                task_filter['deadline'] = timezone.make_aware(datetime.datetime.strptime(deadline, "%Y-%m-%d"))
            except ValueError:
                message["query_param_deadline"] = (f"Incorrect query parameter 'deadline': {deadline}, "
                                                   f"you should enter the deadline date in YYYY-MM-DD format")
                is_error = True

        if page := query_params.get("page"):
            try:
                task_filter["page"] = int(page)
            except ValueError:
                message["query_param_page"] = (f"Incorrect query parameter 'page': {deadline}, "
                                               f"you must enter the page as a number")
                is_error = True

        if is_error:
            raise BadRequestException(message)
        return self.get_tasks(**task_filter)

    def get_tasks(self, *args, **kwargs):
        page_number = None
        if "page" in kwargs:
            page_number = kwargs.pop("page")

        tasks = Task.objects.filter(**kwargs).all()
        if not tasks:
            raise NoContentException()

        if len(tasks) < 2:
            return TaskDetailSerializer(tasks[0]).data

        if page_number:
            try:
                paginator = Paginator(tasks, per_page=self.__PAGE_SIZE)
                tasks = paginator.page(page_number)
            except InvalidPage:
                raise BadRequestException("Invalid page number")

        return TaskDetailSerializer(tasks, many=True).data
