from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from first_app.models.task_manager import Task
from first_app.serializers.task_serializer import TaskDetailSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from first_app.paginations.task_subtask_parination import TaskPagination


class TaskListView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    pagination_class = TaskPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class TaskDetailView(RetrieveUpdateDestroyAPIView):
    """Представление для получения, обновления и удаления задач."""
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
