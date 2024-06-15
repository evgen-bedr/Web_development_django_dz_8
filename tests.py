from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import timedelta
from first_app.models.task_manager import Category, Task, SubTask


class CategoryTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category_data = {'name': 'TestCategory'}
        self.category = Category.objects.create(name='ExistingCategory')

    def test_create_category(self):
        response = self.client.post(reverse('category-create'), self.category_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.get(id=2).name, 'TestCategory')

    def test_create_duplicate_category(self):
        response = self.client.post(reverse('category-create'), {'name': 'ExistingCategory'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_category(self):
        response = self.client.put(reverse('category-update', kwargs={'pk': self.category.id}),
                                   {'name': 'UpdatedCategory'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'UpdatedCategory')

    def test_update_category_with_existing_name(self):
        new_category = Category.objects.create(name='NewCategory')
        response = self.client.put(reverse('category-update', kwargs={'pk': new_category.id}),
                                   {'name': 'ExistingCategory'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TaskAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_task_data = {
            'title': 'Valid Task',
            'description': 'This is a valid task',
            'deadline': (timezone.now() + timedelta(days=1)).isoformat()  # valid future date
        }
        self.invalid_task_data = {
            'title': 'Invalid Task',
            'description': 'This is an invalid task',
            'deadline': (timezone.now() - timedelta(days=1)).isoformat()  # invalid past date
        }
        self.url = reverse('task-create')

    def test_create_task_with_valid_deadline(self):
        response = self.client.post(self.url, self.valid_task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'Valid Task')

    def test_create_task_with_invalid_deadline(self):
        response = self.client.post(self.url, self.invalid_task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('deadline', response.data)
        self.assertEqual(Task.objects.count(), 0)

class SubTaskAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Test Category')
        self.task = Task.objects.create(title='Test Task', description='Test Task Description', deadline='2023-12-31T23:59:59Z')
        self.task.categories.add(self.category)
        self.subtask = SubTask.objects.create(task=self.task, title='Test SubTask', status='new', deadline='2023-12-31T23:59:59Z')
        self.valid_payload = {
            'task': self.task.id,
            'title': 'New SubTask',
            'status': 'new'
        }
        self.invalid_payload = {
            'task': self.task.id,
            'title': '',
            'status': 'new'
        }
        self.subtask_url = reverse('subtask-detail-update-delete', kwargs={'pk': self.subtask.id})
        self.subtask_list_create_url = reverse('subtask-list-create')

    def test_get_all_subtasks(self):
        response = self.client.get(self.subtask_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_valid_subtask(self):
        response = self.client.post(self.subtask_list_create_url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SubTask.objects.count(), 2)

    def test_create_invalid_subtask(self):
        response = self.client.post(self.subtask_list_create_url, data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_valid_single_subtask(self):
        response = self.client.get(self.subtask_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.subtask.title)

    def test_get_invalid_single_subtask(self):
        response = self.client.get(reverse('subtask-detail-update-delete', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_update_subtask(self):
        updated_payload = {
            'task': self.task.id,
            'title': 'Updated SubTask',
            'status': 'in_progress'
        }
        response = self.client.put(self.subtask_url, data=updated_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.subtask.refresh_from_db()
        self.assertEqual(self.subtask.title, 'Updated SubTask')
        self.assertEqual(self.subtask.status, 'in_progress')

    def test_invalid_update_subtask(self):
        response = self.client.put(self.subtask_url, data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_valid_subtask(self):
        response = self.client.delete(self.subtask_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SubTask.objects.count(), 0)

    def test_delete_invalid_subtask(self):
        response = self.client.delete(reverse('subtask-detail-update-delete', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
