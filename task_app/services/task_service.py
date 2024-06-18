import datetime

from task_app.exceptions.task_app_exception import BadRequestException, CreateValidationError
from task_app.repositories.task_repository import TaskRepository
from task_app.serializers.task_serializer import TaskDetailSerializer, TaskCreateSerializer

from django.utils import timezone

from task_app.services.category_service import CategoryService


class TaskService:
    __PAGE_SIZE = 2

    def __init__(self, task_repository: TaskRepository, category_service: CategoryService):
        self.__task_repository = task_repository
        self.__category_service = category_service

    def get_all_tasks(self):
        tasks = self.__task_repository.get_all_tasks()
        serializer = TaskDetailSerializer(tasks, many=True)
        return serializer.data

    def create_new_task(self, task_data: dict):
        categories = []
        if "categories" in task_data:
            categories_data = task_data.pop("categories")
            categories = self.__category_service.check_if_names_contains_in_categories(categories_data)

        serializer = TaskCreateSerializer(data=task_data)
        if not serializer.is_valid(raise_exception=True):
            raise CreateValidationError(serializer.errors)

        task = self.__task_repository.create_task(**serializer.validated_data)
        print("Task ID", task.id)
        task.categories.add(*categories)
        serializer = TaskDetailSerializer(task)

        return serializer.data

    def get_task_by_pk(self, task_pk: int):
        task = self.__task_repository.get_task_by_id(task_pk)
        serializer = TaskDetailSerializer(task)
        return serializer.data

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
        tasks = self.__task_repository.get_all_tasks_by_filter(**task_filter)
        serializer = TaskDetailSerializer(data=tasks, many=True)
        return serializer.data
