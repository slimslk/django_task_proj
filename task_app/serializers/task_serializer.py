from rest_framework import serializers

from task_app.models import Task, Category
from task_app.serializers.category_serializer import CategorySerializer


class TaskCategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

    class Meta:
        # model = Category
        fields = [
            "name"
        ]


class TaskSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, required=False)
    categories_name = TaskCategorySerializer(
        write_only=True,
        required=False,
        many=True
    )

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "status",
            "deadline",
            "categories",
            "categories_name"
        ]

        read_only_fields = [
            "categories"
        ]

    def create(self, validated_data):
        if "categories_name" in validated_data:
            categories_data = validated_data.pop("categories_name")
            task = Task.objects.create(**validated_data)
            print(categories_data)
            for category_data in categories_data:
                category, created = Category.objects.get_or_create(
                    name=category_data.get("name")
                )
                category.tasks.add(task)
                category.save()
        else:
            task = Task.objects.create(**validated_data)
        return task
