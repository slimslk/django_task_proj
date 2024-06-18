from rest_framework import serializers

from task_app.models import Subtask


class SubTaskCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subtask
        fields = "__all__"
        read_only_fields = ["created_at"]


class SubTaskDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subtask
        fields = [
            "title",
            "description",
            "status",
            "deadline",
            "created_at",
        ]
        read_only_fields = [
            "created_at",
        ]
