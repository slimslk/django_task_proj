from task_app.exceptions.task_app_exception import CreateValidationError, BadRequestException
from task_app.models import Category
from task_app.repositories.category_repository import CategoryRepository
from task_app.serializers.category_serializer import CategoryDetailSerializer, CategoryCreateSerializer


class CategoryService:

    def __init__(self, category_repository: CategoryRepository):
        self.__category_repository = category_repository

    def create_category(self, category_data):
        serializer = CategoryCreateSerializer(data=category_data)
        if not serializer.validated_data():
            raise CreateValidationError(serializer.errors)
        category = self.__category_repository.create_category(**serializer.validated_data)
        return CategoryDetailSerializer(data=category)

    def get_all_categories(self):
        categories = self.__category_repository.get_all_categories()
        serializer = CategoryDetailSerializer(categories, many=True)
        return serializer.data

    def get_category_by_name(self, category_name: str):
        category = self.__category_repository.get_category_by_name(category_name)
        serializer = CategoryDetailSerializer(category)
        return serializer.data

    def get_category_by_id(self, category_id: int) -> Category:
        category = self.__category_repository.get_category_by_id(category_id)
        serializer = CategoryDetailSerializer(category)
        return serializer.data

    def delete_category_by_id(self, category_id: int) -> str:
        self.__category_repository.delete_category_by_id(category_id)
        return "Successful deleted."

    def check_if_names_contains_in_categories(self, categories_data: dict[str: str]) -> list[Category]:

        all_categories = self.__category_repository.get_all_categories()
        serializer = CategoryDetailSerializer(all_categories, many=True)
        if not all(category in serializer.data for category in categories_data):
            raise BadRequestException(
                "Some of the categories are not existed. Please add only existed categories."
            )
        categories = []
        for category in all_categories:
            if category.name in [cat.get("name") for cat in categories_data]:
                categories.append(category)

        return categories


