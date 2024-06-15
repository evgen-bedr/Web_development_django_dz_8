from django.urls import path
from first_app.views.task_views import (
    get_tasks_by_status_and_deadline,
    get_tasks_statistic,
    get_all_tasks,
    create_task
)
from first_app.views.sub_task_views import (
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView
)
from first_app.views.category_views import CategoryCreateView, CategoryUpdateView

urlpatterns = [
    path('tasks/', get_tasks_by_status_and_deadline),
    path('tasks/all/', get_all_tasks),
    path('tasks/create/', create_task, name='task-create'),
    path('tasks/statistic/', get_tasks_statistic),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/update/<int:pk>/', CategoryUpdateView.as_view(), name='category-update'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
]