from django.test import TestCase

from task_app.repositories.category_repository import CategoryRepository
from task_app.repositories.task_repository import TaskRepository
from task_app.services.category_service import CategoryService
from task_app.services.task_service import TaskService


class TestTaskService(TestCase):

    # TODO: Mock 3 fields below
    __task_repository = TaskRepository()
    __category_repository = CategoryRepository()
    __category_service = CategoryService(category_repository=__category_repository)

    __task_service = TaskService(task_repository=__task_repository, category_service=__category_service)

    def test_get_all_tasks(self):
        self.fail()

    def test_create_new_task(self):
        self.fail()

    def test_get_task_by_pk(self):
        self.fail()

    def test_filter_tasks_by_query_params(self):
        self.fail()
