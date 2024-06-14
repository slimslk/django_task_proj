from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from task_app.models import Category
from task_app.serializers.category_serializer import CategorySerializer, CategoryCreateSerializer


class CategorySerializerTest(TestCase):

    def setUp(self):
        cat1 = Category.objects.create(
            name="IT"
        )
        cat2 = Category.objects.create(
            name="QA"
        )
        cat3 = Category.objects.create(
            name="DevOps"
        )

        self.category_id = cat3.id

        self.categories = [
            cat1, cat2, cat3
        ]
        self.expected = CategorySerializer(self.categories, many=True)

    def test_get_all_categories(self):
        categories = Category.objects.all()
        actual = CategorySerializer(categories, many=True)
        self.assertEqual(actual.data, self.expected.data)

    def test_get_category_by_id(self):
        category = Category.objects.get(pk=self.category_id)
        actual = CategorySerializer(category)
        self.assertEqual(actual.data, self.expected.data[2])

    def test_get_by_id_if_not_exist(self):
        with self.assertRaises(ObjectDoesNotExist) as cm:
            Category.objects.get(pk=-1)
        the_exception = cm.exception
        self.assertEqual(the_exception.__class__.__name__, Category.DoesNotExist.__name__)

    def test_create_new_category(self):
        data = {"name": "Barista"}
        expected = CategoryCreateSerializer(data=data)
        expected.is_valid()
        expected.save()
        actual = Category.objects.filter(name="Barista").values("id", "name").first()
        self.assertDictEqual(actual, expected.data, f"{actual}, {expected.data}")

    def test_error_when_create_category_if_name_is_existed(self):
        Category.objects.create(name="CEO")
        with self.assertRaises(ValidationError) as err:
            data = {"name": "CEO"}
            category = CategoryCreateSerializer(data=data)
            if category.is_valid():
                category.save()
        the_exception = err.exception
        self.assertEqual(the_exception.__class__.__name__, ValidationError.__name__)

    def test_error_when_update_category_if_name_is_existed(self):
        category = Category.objects.get(pk=self.category_id)
        with self.assertRaises(ValidationError) as err:
            data = {"name": "QA"}
            category = CategoryCreateSerializer(instance=category, data=data)
            if category.is_valid():
                category.save()
        the_exception = err.exception
        self.assertEqual(the_exception.__class__.__name__, ValidationError.__name__)

    def test_update_by_id(self):
        category = Category.objects.get(pk=self.category_id)
        update_data = {"name": "PM"}
        expected = CategoryCreateSerializer(instance=category, data=update_data)
        if expected.is_valid():
            expected.save()
        actual = Category.objects.values("id", "name").get(pk=self.category_id)
        self.assertEqual(actual, expected.data)

    def test_delete_category_by_id(self):
        category = Category.objects.get(pk=self.category_id)
        category.delete()
        actual = Category.objects.filter(pk=self.category_id).first()
        self.assertEqual(actual, None)
