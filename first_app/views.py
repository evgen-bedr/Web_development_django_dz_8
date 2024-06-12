from rest_framework.request import Request
from rest_framework.response import Response
from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import api_view
from django.utils import timezone
from first_app.models.task_manager import Task
from first_app.serializers.tasks import AllTaskSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class TaskPagination(Paginator):
    def get_paginated_data(self, page_number):
        try:
            page_obj = self.page(page_number)
        except EmptyPage:
            page_obj = self.page(self.num_pages)
        except PageNotAnInteger:
            page_obj = self.page(1)
        return page_obj


@api_view(['GET'])
def get_tasks_by_status_and_deadline(request: Request) -> Response:
    task_status = request.query_params.get('status')
    task_deadline = request.query_params.get('deadline')

    if not (task_status and task_deadline):
        return Response({'Нет статуса или дедлайна'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        task_deadline = timezone.datetime.strptime(task_deadline, '%Y-%m-%d').date()
    except ValueError:
        return Response({'Не правильный формат YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)

    tasks = Task.objects.filter(status=task_status, deadline__date=task_deadline).order_by('deadline')

    paginator = TaskPagination(tasks, 2)  # Указание размера страницы здесь
    paginated_tasks = paginator.get_paginated_data(request.query_params.get('page', 1))

    serializer = AllTaskSerializer(paginated_tasks, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def get_tasks_statistic(request: Request) -> Response:
    tasks_count = Task.objects.count()
    tasks_by_status = Task.objects.values('status').annotate(tasks_count=Count('id')).order_by('status')

    now = timezone.now()
    done_tasks = Task.objects.filter(status='done').count()
    overdue_tasks_count = Task.objects.filter(deadline__lt=now).count() - done_tasks

    return Response({'tasks_count': tasks_count} | {'tasks_by_status': tasks_by_status} | {
        'overdue_tasks_count': overdue_tasks_count})
