from django.db import models

from task_app.constants.choices import StatusChoices


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField('Category', related_name='tasks')
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.NEW)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "task_manager_task"
        ordering = ('-created_at',)
        verbose_name = 'Task'
        verbose_name_plural = 'Task'
        unique_together = ("title", "created_at")

    def __str__(self):
        return self.title
