from datetime import datetime, timedelta
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from first_app.models.task_manager import Task, SubTask

"""
    1. Создание записей:

    Task:
        title: "Prepare presentation".
        description: "Prepare materials and slides for the presentation".
        status: "New".
        deadline: Today's date + 3 days.
"""

deadline_date = datetime.now().date() + timedelta(days=3)
deadline_str = deadline_date.strftime('%Y-%m-%d')

new_task = Task.objects.create(
    title="End 2",
    description="Prepare",
    status="done",
    deadline="2025-12-11"
)

"""
    1.2 SubTasks для "Prepare presentation":

    title: "Gather information".
    description: "Find necessary information for the presentation".
    status: "New".
    deadline: Today's date + 2 days.
        
    title: "Create slides".
    description: "Create presentation slides".
    status: "New".
    deadline: Today's date + 1 day.
"""

deadline_date = datetime.now().date() + timedelta(days=2)
deadline_str = deadline_date.strftime('%Y-%m-%d')

new_subtask = SubTask.objects.create(
    title="Gather information",
    description="Find necessary information for the presentation",
    status="New",
    deadline=deadline_str,
    task_id=6
)

deadline_date = datetime.now().date() + timedelta(days=1)
deadline_str = deadline_date.strftime('%Y-%m-%d')

new_subtask = SubTask.objects.create(
    title="Create slides",
    description="Create presentation slides",
    status="New",
    deadline=deadline_str,
    task_id=6
)

"""
    2. Чтение записей:

    Tasks со статусом "New":
        Вывести все задачи, у которых статус "New".
        
    SubTasks с просроченным статусом "Done":
        Вывести все подзадачи, у которых статус "Done", но срок выполнения истек.
"""

tasks_status = Task.objects.filter(status__iexact="New")
subtask_status = SubTask.objects.filter(status__iexact="Done")

"""
    3. Изменение записей:

    Измените статус "Prepare presentation" на "In progress".
    Измените срок выполнения для "Gather information" на два дня назад.
    Измените описание для "Create slides" на "Create and format presentation slides".
"""

task_status_change = Task.objects.filter(title="Prepare presentation").update(status="In progress")

sub_task = SubTask.objects.get(title="Gather information")
new_deadline = sub_task.deadline - timedelta(days=2)
sub_task.deadline = new_deadline
sub_task.save()

sub_task = SubTask.objects.filter(title="Create slides").update(description="Create and format presentation slides")

"""
    4. Удаление записей:

    Удалите задачу "Prepare presentation" и все ее подзадачи.
"""

task = Task.objects.get(title="Prepare presentation")
task.delete()
