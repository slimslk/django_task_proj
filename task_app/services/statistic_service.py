from django.db.models import Count, Subquery, Value
from django.utils import timezone

from task_app.exceptions.task_app_exception import NoContentException
from task_app.models import Task


class StatisticService:

    def get_task_statistic(self):
        result = {}
        overdue_tasks_subquery = Task.objects.filter(
            deadline__lt=timezone.now()
        ).annotate(
            dummy=Value(1)
        ).values(
            "dummy"
        ).annotate(overdue_tasks=Count("dummy")).values("overdue_tasks")

        total_tasks_subquery = Task.objects.annotate(
            dummy=Value(1)
        ).values(
            'dummy'
        ).annotate(total_tasks=Count('dummy')).values('total_tasks')

        queryset = Task.objects.values(
            "status"
        ).annotate(
            total_tasks=Subquery(total_tasks_subquery),
            overdue_tasks=Subquery(overdue_tasks_subquery),
            total_tasks_by_status=Count("status")
        ).values("status", "total_tasks_by_status", "total_tasks", "overdue_tasks")

        statistic = list(queryset)
        result["total_tasks"] = statistic[0].get("total_tasks")
        result["overdue_tasks"] = statistic[0].get("overdue_tasks")
        tasks_by_status = [{status.get("status"): status.get("total_tasks_by_status")} for status in statistic]
        result["total_tasks_by_status"] = tasks_by_status
        if not result:
            raise NoContentException()

        return result

