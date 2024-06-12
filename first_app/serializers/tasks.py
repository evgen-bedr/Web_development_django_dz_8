from rest_framework import serializers
from first_app.models.task_manager import Task


class AllTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']