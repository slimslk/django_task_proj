from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from task_app.models import Category
from task_app.serializers.category_serializer import CategoryCreateSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer

    @action(detail=False, methods=["GET"], url_path='count')
    def count_tasks(self, request: Request) -> Response:
        task_count = list(Category.objects.annotate(amount_of_tasks=Count("tasks")).values("name", "amount_of_tasks"))
        total_tasks = sum(item.get("amount_of_tasks", 0) for item in task_count)
        task_count.append({"total_tasks": total_tasks})
        return Response(data=task_count, status=status.HTTP_200_OK)
