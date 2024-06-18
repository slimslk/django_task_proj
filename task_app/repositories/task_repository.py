from django.core.paginator import Paginator, InvalidPage
from django.db.utils import IntegrityError

from task_app.exceptions.task_app_exception import NothingToUpdateException, BadRequestException, NoContentException
from task_app.models import Task, Category
from task_app.constants.model_constants import TASK_FIELDS
from task_app.utils.repository_helper import prepare_instance_to_update


class TaskRepository:
    __PAGE_SIZE = 3

    def get_all_tasks(self) -> list[Task]:
        return self.__get_tasks()

    def get_task_by_id(self, task_id: int) -> Task:
        return self.__get_tasks(pk=task_id)

    def get_all_tasks_by_filter(self, filter_data: dict[str]) -> list[Task]:
        return self.__get_tasks(**filter_data)

    def create_task(self, **task_data) -> Task:
        task = Task(**task_data)
        try:
            task.save()
        except IntegrityError as err:
            raise BadRequestException(str(err))
        return task

    def update_task(self, task_id: int,**task_data) -> Task:
        task: Task = self.__get_tasks(pk=task_id)
        try:
            task, update_fields = prepare_instance_to_update(task_data, task, TASK_FIELDS)
            if not update_fields:
                raise NothingToUpdateException()
            task.save(update_fields=update_fields)
        except IntegrityError as err:
            raise BadRequestException(str(err))
        return task

    def delete_task(self, task_id):
        Task.objects.filter(pk=task_id).delete()

    def __get_tasks(self, *args, **kwargs):
        page_number = None

        if "page" in kwargs:
            page_number = kwargs.pop("page")

        tasks = Task.objects.filter(**kwargs)
        if not tasks:
            raise NoContentException()

        if len(tasks) < 2:
            return tasks.first()

        if page_number:
            try:
                paginator = Paginator(tasks, per_page=self.__PAGE_SIZE)
                tasks = paginator.page(page_number)
            except InvalidPage:
                raise BadRequestException("Invalid page number")

        return tasks
