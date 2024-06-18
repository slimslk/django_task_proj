from task_app.models import Subtask


class SubtaskRepository:

    def get_all_subtasks(self):
        return Subtask.objects.all()