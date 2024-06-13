from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from task_app.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]


class CategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"

    def create(self, validated_data):
        name = validated_data.get("name")
        if Category.objects.exists(name):
            raise ValidationError(f"{name} is existed. Category name should be unique.")

        return Category(**validated_data)

    def update(self, instance, validated_data):
        if "name" in validated_data:
            name = validated_data.get("name")
            if Category.objects.exists(name):
                raise ValidationError(f"{name} is existed. Category name should be unique.")

            instance.name = name
        return instance




