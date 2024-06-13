from datetime import datetime

from rest_framework import serializers
from django.utils import timezone

from task_app.exceptions.task_app_exception import BadRequestException
from task_app.models import Task, Category
from task_app.serializers.category_serializer import CategorySerializer
from task_app.serializers.sub_task_serializer import SubTaskDetailSerializer


class TaskCategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

    class Meta:
        fields = [
            "name"
        ]


class TaskCreateSerializer(serializers.ModelSerializer):
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

    def validate_deadline(self, value):
        try:
            if timezone.make_aware(datetime.strptime(str(value), "%Y-%m-%d %H:%M:%S+00:00")) < timezone.now():
                raise serializers.ValidationError(f"Deadline date {value} cannot be at the past.")
            return value
        except ValueError as err:
            raise BadRequestException(str(err))

    def create(self, validated_data):
        if "categories_name" in validated_data:
            categories_data = validated_data.pop("categories_name")
            task = Task.objects.create(**validated_data)
            for category_data in categories_data:
                category, created = Category.objects.get_or_create(
                    name=category_data.get("name")
                )
                category.tasks.add(task)
                category.save()
        task = Task.objects.create(**validated_data)

        return task


class TaskDetailSerializer(serializers.ModelSerializer):

    subtasks = SubTaskDetailSerializer(many=True, read_only=True)

    categories = serializers.StringRelatedField(many=True)

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "status",
            "deadline",
            "categories",
            "subtasks",
            "created_at"
        ]
        read_only_fields = [
            "created_at",
            "categories"
        ]
