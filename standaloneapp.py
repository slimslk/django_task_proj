import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import timezone
from django.db.models import Q, F, QuerySet

from task_app.models import Task, SubTask, Category
from task_app.constants import model_constants as constants


# 1. Создание записей:
def create_records():
    task = Task(
        title="Prepare presentation",
        description="Prepare materials and slides for the presentation",
        status=constants.STATUS_CHOICES[0][0],
        deadline=timezone.now() + timezone.timedelta(days=3)
    )
    task.save()

    sub_tasks = [
        SubTask(
            task=task,
            title="Gather information",
            description="Find necessary information for the presentation",
            status=constants.STATUS_CHOICES[0][0],
            deadline=timezone.now() + timezone.timedelta(days=2)
        ),
        SubTask(
            task=task,
            title="Create slides",
            description="Create presentation slides",
            status=constants.STATUS_CHOICES[0][0],
            deadline=timezone.now() + timezone.timedelta(days=1)
        )
    ]

    SubTask.objects.bulk_create(sub_tasks)


# 2. Чтение записей:
def read_records():
    tasks: Task = Task.objects.filter(status__exact=constants.STATUS_CHOICES[0][0])
    print(tasks)

    sub_tasks: SubTask = SubTask.objects.filter(
        Q(status__exact=constants.STATUS_CHOICES[4][0]) & Q(deadline__lt=timezone.now())
    )
    print(sub_tasks)


# 3. Изменение записей:
def update_records():
    try:
        task: Task = Task.objects.get(title="Prepare presentation")
        task.status = constants.STATUS_CHOICES[1][0]
        task.save()

        sub_task_gather_info: QuerySet = SubTask.objects.filter(title__exact="Gather information")
        sub_task_gather_info.update(deadline=F('deadline') - timezone.timedelta(days=2))

        sub_task_create_slides: SubTask = SubTask.objects.filter(title="Create slides").first()
        sub_task_create_slides.description = "Create and format presentation slides"
        sub_task_create_slides.save()

    except (Task.DoesNotExist, Task.MultipleObjectsReturned):
        print("Not found or multiple records returned")


# 4. Удаление записей:
def delete_records():
    task: Task = Task.objects.filter(title__exact="Prepare presentation").first()
    task.delete()


if __name__ == "__main__":
    create_records()
    read_records()
    update_records()
    delete_records()
