from django.test import TestCase

from task_app.repositories.category_repository import CategoryRepository
from task_app.serializers.category_serializer import CategoryDetailSerializer, CategoryCreateSerializer


class CategorySerializerTest(TestCase):

    # TODO: Mock field __category_repository
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

        self.category_id = cat3.id

        self.categories = [
            cat1, cat2, cat3
        ]
        self.expected = CategoryDetailSerializer(self.categories, many=True)

    def test_CategoryDetailSerializer_with_may_records(self):
        categories = self.__category_repository.get_all_categories()
        actual = CategoryDetailSerializer(categories, many=True)
        self.assertCountEqual(actual.data, self.expected.data)

    def test_CategoryDetailSerializer_with_one_record(self):
        category = self.__category_repository.get_category_by_id(self.category_id)
        actual = CategoryDetailSerializer(category)
        self.assertEqual(actual.data, self.expected.data[2])

    def test_CategoryCreateSerializer(self):
        data = {"name": "Barista"}
        expected = CategoryCreateSerializer(data=data)
        expected.is_valid()
        validated_category_data = expected.validated_data
        category = self.__category_repository.create_category(**validated_category_data)
        category_id = category.id
        actual = self.__category_repository.get_category_by_id(category_id)
        self.assertEqual(actual, category, f"{actual}, {expected.data}")


