from django.db import models

from task_app.constants.choices import StatusChoices


class Subtask(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    task = models.ForeignKey('Task', related_name='subtasks', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.NEW)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "task_manager_subtask"
        ordering = ('-created_at',)
        verbose_name = 'Sub Task'
        verbose_name_plural = 'Sub Task'
        unique_together = ("title",)