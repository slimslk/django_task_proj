from django.db.utils import IntegrityError

from task_app.constants.model_constants import CATEGORY_FIELDS
from task_app.exceptions.task_app_exception import BadRequestException, NoContentException, NothingToUpdateException
from task_app.models import Category
from task_app.utils.repository_helper import prepare_instance_to_update


class CategoryRepository:

    def get_all_categories(self) -> list[Category]:
        return self.__get_categories()

    def get_category_by_id(self, category_id: int) -> Category:
        return self.__get_categories(pk=category_id)

    def get_category_by_name(self, category_name: str) -> Category:
        return self.__get_categories(name=category_name)

    def create_category(self, **category_data):
        category = Category(**category_data)
        try:
            category.save()
        except IntegrityError as err:
            raise BadRequestException(str(err))
        return category

    def update_category(self, category_id: int, **category_data) -> Category:
        category: Category = self.__get_categories(pk=category_id)
        try:
            category, update_fields = prepare_instance_to_update(category_data, category, CATEGORY_FIELDS)
            if not update_fields:
                raise NothingToUpdateException()
            category.save(update_fields=update_fields)
        except IntegrityError as err:
            raise BadRequestException(str(err))
        return category

    def delete_category_by_id(self, category_id: int):
        Category.objects.filter(pk=category_id).delete()

    def __get_categories(self, *args, **kwargs) -> list[Category] | Category:
        categories = Category.objects.filter(**kwargs)
        if not categories:
            raise NoContentException()

        if len(categories) < 2:
            return categories.first()
        return categories
