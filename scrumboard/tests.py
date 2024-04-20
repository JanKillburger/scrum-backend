from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from scrumboard.models import Task


class TaskModelTests(TestCase):
    def test_default_open_status(self):
        task = Task(
            {
                "title": "Test title",
                "description": "Test desc",
                "due_date": "2024-04-28",
                "assigned_to": 1,
            }
        )
        self.assertIs(task.status, "open")


class TaskViewTests(TestCase):
    def test_unauthenticated_user(self):
        client = APIClient()
        response = client.get("/tasks/")
        self.assertIs(response.status_code, 401)

    def test_authenticated_user(self):
        user = User.objects.create_user("testuser")
        token = Token.objects.create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Token  {token.key}")
        response = client.get("/tasks/")
        self.assertIs(response.status_code, 200)
