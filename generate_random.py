import os
import django
import random
from faker import Faker
from datetime import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from first_app.models.task_manager import Task, SubTask, Category

fake = Faker()

STATUS_CHOICES = ['new', 'in_progress', 'pending', 'blocked', 'done']


def create_categories(n=5):
    categories = []
    for _ in range(n):
        name = fake.word()
        category, created = Category.objects.get_or_create(name=name)
        categories.append(category)
    return categories


def create_tasks(n=10, categories=None):
    tasks = []
    for _ in range(n):
        title = fake.sentence(nb_words=4)
        description = fake.text()
        status = random.choice(STATUS_CHOICES)
        deadline = fake.date_time_between(start_date='-1y', end_date='+1y', tzinfo=timezone.utc)
        task = Task.objects.create(title=title, description=description, status=status, deadline=deadline)
        if categories:
            task.categories.set(random.sample(categories, random.randint(1, len(categories))))
        tasks.append(task)
    return tasks


def create_subtasks(n=20, tasks=None):
    for _ in range(n):
        title = fake.sentence(nb_words=4)
        description = fake.text()
        status = random.choice(STATUS_CHOICES)
        deadline = fake.date_time_between(start_date='-1y', end_date='+1y', tzinfo=timezone.utc)
        task = random.choice(tasks)
        SubTask.objects.create(title=title, description=description, status=status, deadline=deadline, task=task)


if __name__ == '__main__':
    categories = create_categories()
    tasks = create_tasks(categories=categories)
    create_subtasks(tasks=tasks)
    print('Database populated successfully!')
