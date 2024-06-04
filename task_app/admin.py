from django.contrib import admin

from task_app.models.category import Category
from task_app.models.task import Task, SubTask


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ('title', 'status', 'deadline')
    list_filter = ('status', 'categories')
    list_display = ('title', 'status', 'get_categories_name', 'created_at', 'deadline')

    def get_categories_name(self, obj: Task):
        categories_name = ", ".join(cat.name for cat in obj.categories.all())
        return categories_name

    get_categories_name.short_description = "Categories"


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    search_fields = ('title', 'status', 'deadline')
    list_filter = ('status',)
    list_display = ('title', 'task', 'status', 'created_at', 'deadline')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)
