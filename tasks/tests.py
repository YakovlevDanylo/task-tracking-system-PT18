from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.utils import timezone

from tasks.forms import TaskForm
from tasks.models import Task


# Create your tests here.
class TaskFormTest(TestCase):

    def test_form_valid(self):
        form = TaskForm(data={"title": "New Title",
                              "description": "New Description",
                              "status": "todo",
                              "priority": "low_priority",
                              "end_time": timezone.now()
                              })
        self.assertTrue(form.is_valid())

class TaskListViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_task_list_view_load(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

class TaskCreateViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_task_create_view_get(self):
        self.client.force_login(self.user)

        response = self.client.get("/create-task/")
        self.assertEqual(response.status_code, 200)

    def test_task_create_view_post(self):
        self.client.force_login(self.user)

        response = self.client.post("/create-task/",
                        {"title": "New Title",
                              "description": "New Description",
                              "status": "todo",
                              "priority": "low_priority",
                              })

        self.assertEqual(Task.objects.count(), 1)

