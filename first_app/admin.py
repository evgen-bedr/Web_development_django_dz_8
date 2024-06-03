from django.contrib import admin
from first_app.models import Task, SubTask, Category


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'status', 'formatted_deadline', 'formatted_created_at')
    search_fields = ('title', 'description')
    list_filter = ('deadline',)
    ordering = ('-created_at', 'title')
    list_per_page = 10


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'task', 'status', 'formatted_deadline', 'formatted_created_at')
    search_fields = ('title', 'description')
    list_filter = ('deadline',)
    ordering = ('-created_at', 'title')
    list_per_page = 10


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('-name',)
    list_per_page = 10
