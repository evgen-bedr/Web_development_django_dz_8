from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from first_app.views.task_views import (
    get_tasks_by_status_and_deadline,
    get_tasks_statistic,
    get_all_tasks,
    create_task,
    TaskCreateView,
    TaskListView,
    GenreDetailUpdateDeleteView,
    TaskListCreateView,
    TaskDetailDeleteUpdateView
)
from first_app.views.sub_task_views import (
    SubTaskListCreateWithPermissionView,
    SubTaskDetailDeleteUpdateView
)

from first_app.views.auth_views import (
    AuthView,
    LoginUserView,
    LogoutUserView,
    RegisterUserView
)

from first_app.views.task_generic_view import TaskListView, TaskDetailView
from first_app.views.sub_task_generic_view import (
    SubTaskListView,
    SubTaskDetailView
)
from first_app.views.category_views import (
    CategoryCreateView,
    CategoryUpdateView,
    CategoryViewSet
)

router = DefaultRouter()
task_router = DefaultRouter()
subtask_router = DefaultRouter()

router.register(r'', CategoryViewSet)
task_router.register(r'', TaskListCreateView, basename='tasks')
subtask_router.register(r'', SubTaskListCreateWithPermissionView, basename='subtasks')

urlpatterns = [
    path('categories/', include(router.urls)),
    path('tasks/', include(task_router.urls)),
    path('subtasks/', include(subtask_router.urls)),

    path('tasks/<int:pk>/', TaskDetailDeleteUpdateView.as_view(), name='task-detail'),
    path('tasks/create/', create_task, name='task-create'),
    path('tasks/statistic/', get_tasks_statistic),
    path('tasks/all/', get_all_tasks),
    path('tasks/create/v2/', TaskCreateView.as_view(), name='task-class-create'),
    path('tasks/create/v3/', TaskListView.as_view(), name='task-list-create'),
    path('tasks/create/v4/', TaskListView.as_view(), name='task-generic-list'),
    path('tasks/create/v4/<int:pk>/', TaskDetailView.as_view(), name='task-generic-detail'),

    path('subtasks/<int:pk>/', SubTaskDetailDeleteUpdateView.as_view(), name='subtask-detail'),
    path('subtasks/create/', SubTaskListCreateWithPermissionView.as_view({'post': 'create'}), name='subtask-create'),
    path('subtasks/create/v4/<int:pk>/', SubTaskDetailView.as_view(), name='subtask-generic-detail'),

    path('protected/', AuthView.as_view(), name='protected'),
    path('register/', RegisterUserView.as_view(), name='user_register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('jwt-auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt-refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/update/<int:pk>/', CategoryUpdateView.as_view(), name='category-update'),
    path('genres/<str:genre_name>/', GenreDetailUpdateDeleteView.as_view(), name='genre-detail-update-delete'),
]
