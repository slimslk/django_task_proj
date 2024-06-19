from rest_framework import serializers

from task_app.models import Subtask


class SubtaskCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subtask
        fields = "__all__"
        read_only_fields = ["created_at"]


class SubtaskDetailSerializer(serializers.ModelSerializer):

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
