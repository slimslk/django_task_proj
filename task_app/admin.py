from django.contrib import admin

from task_app.models.category import Category
from task_app.models.task import Task, SubTask

# Register your models here.
admin.site.register(Category)
admin.site.register(Task)
admin.site.register(SubTask)
