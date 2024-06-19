from django.db.models import QuerySet

from task_app.exceptions.task_app_exception import NoContentException, CreateValidationError
from task_app.models import Subtask
from task_app.repositories.subtask_repository import SubtaskRepository
from task_app.serializers.subtask_serializer import SubtaskDetailSerializer, SubtaskCreateSerializer


class SubtaskService:
    
    def __init__(self, subtask_repository: SubtaskRepository):
        self.__subtask_repository = subtask_repository

    def get_all_subtask(self):
        return self.get_tasks()

    def create_new_task(self, subtask_data):
        serializer = SubtaskCreateSerializer(data=subtask_data)
        if not serializer.is_valid(raise_exception=True):
            raise CreateValidationError(serializer.errors)

        serializer.save()
        return serializer.data

    def get_subtask_by_id(self, subtask_id):
        return self.get_tasks(pk=subtask_id)

    def update_subtask(self, data, subtask_id):
        subtask = self.__check_subtask_existed(pk=subtask_id).first()
        serializer = SubtaskCreateSerializer(instance=subtask, data=data, partial=True)
        if not serializer.is_valid():
            raise CreateValidationError(serializer.errors)

        serializer.save()
        return serializer.data

    def delete(self, subtask_id):
        if subtask := self.__check_subtask_existed(pk=subtask_id):
            subtask.delete()
        return "Successful deleted."

    def get_tasks(self, *args, **kwargs):
        subtask = self.__check_subtask_existed(**kwargs)

        if len(subtask) < 2:
            return SubtaskDetailSerializer(subtask[0]).data

        return SubtaskDetailSerializer(subtask, many=True).data

    def __check_subtask_existed(self, **kwargs) -> QuerySet:
        subtasks = Subtask.objects.filter(**kwargs).all()
        if not subtasks:
            raise NoContentException()
        return subtasks
