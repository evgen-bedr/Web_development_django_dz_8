from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from first_app.models.task_manager import SubTask
from first_app.serializers.sub_task_serializer import SubTaskSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from first_app.paginations.task_subtask_parination import TaskPagination


class SubTaskListView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    pagination_class = TaskPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class SubTaskDetailView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
