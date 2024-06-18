from datetime import datetime

from rest_framework import serializers
from django.utils import timezone

from task_app.exceptions.task_app_exception import BadRequestException
from task_app.models import Task
from task_app.serializers.subtask_serializer import SubTaskDetailSerializer


class TaskCreateCategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)

    class Meta:
        fields = ["name"]


class TaskCreateSerializer(serializers.ModelSerializer):

    categories = TaskCreateCategorySerializer(many=True, required=False, write_only=True)
    
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "status",
            "deadline",
            "categories",
        ]

    def validate_deadline(self, value):
        try:
            if timezone.make_aware(datetime.strptime(str(value), "%Y-%m-%d %H:%M:%S+00:00")) < timezone.now():
                raise serializers.ValidationError(f"Deadline date {value} cannot be at the past.")
            return value
        except ValueError as err:
            raise BadRequestException(str(err))


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskDetailSerializer(many=True, read_only=True)

    categories = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

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
        ]
