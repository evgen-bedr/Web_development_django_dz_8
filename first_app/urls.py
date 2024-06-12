from django.urls import path
from first_app.views import get_tasks_by_status_and_deadline, get_tasks_statistic

urlpatterns = [
    path('tasks/', get_tasks_by_status_and_deadline),
    path('tasks/statistic/', get_tasks_statistic),
]