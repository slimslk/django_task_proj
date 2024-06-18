from django.test import TestCase

from task_app.exceptions.task_app_exception import BadRequestException, NoContentException
from task_app.repositories.category_repository import CategoryRepository


class TestCategoryRepository(TestCase):

    __category_repository = CategoryRepository()

    def setUp(self):
        cat1 = self.__category_repository.create_category(
            name="IT"
        )
        cat2 = self.__category_repository.create_category(
            name="QA"
        )
        cat3 = self.__category_repository.create_category(
            name="DevOps"
        )

        self.category_id = cat1.id
        self.created_categories = [cat1, cat2, cat3]

    def test_get_all_categories(self):
        actual_categories = self.__category_repository.get_all_categories()
        self.assertCountEqual(self.created_categories, list(actual_categories))

    def test_get_category_by_id(self):
        actual_category = self.__category_repository.get_category_by_id(self.category_id)
        self.assertEqual(self.created_categories[0], actual_category)

    def test_raise_error_when_category_is_not_exist(self):
        with self.assertRaises(NoContentException) as err:
            self.__category_repository.get_category_by_id(-1)
        the_exception = err.exception
        self.assertEqual(the_exception.__class__.__name__, NoContentException.__name__)

    def test_raise_error_when_create_category_if_name_is_existed(self):
        self.__category_repository.create_category(name="CEO")
        with self.assertRaises(BadRequestException) as err:
            self.__category_repository.create_category(name="CEO")
        the_exception = err.exception
        self.assertEqual(the_exception.__class__.__name__, BadRequestException.__name__)

    def test_create_category(self):
        category_data = {"name": "Hacker"}
        created_category = self.__category_repository.create_category(**category_data)
        created_category_id = created_category.id
        actual_category = self.__category_repository.get_category_by_id(created_category_id)
        self.assertEqual(created_category, actual_category)

    def test_raise_error_when_update_category_if_name_is_existed(self):
        with self.assertRaises(BadRequestException) as err:
            data = {"name": "QA"}
            self.__category_repository.update_category(self.category_id, **data)
        the_exception = err.exception
        self.assertEqual(the_exception.__class__.__name__, BadRequestException.__name__)

    def test_update_by_id(self):
        update_data = {"name": "PM"}
        self.__category_repository.update_category(self.category_id, **update_data)
        actual_category = self.__category_repository.get_category_by_id(self.category_id)
        self.assertEqual(actual_category.name, update_data.get("name"))

    def test_delete_category_by_id(self):
        self.__category_repository.delete_category_by_id(self.category_id)
        with self.assertRaises(NoContentException) as err:
            self.__category_repository.get_category_by_id(self.category_id)
        the_exception = err.exception
        self.assertEqual(the_exception.__class__.__name__, NoContentException.__name__)
