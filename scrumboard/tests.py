from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from scrumboard.models import SubTask, Task

def get_authenticated_client():
    user = User.objects.create_user("testuser")
    token = Token.objects.create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token  {token.key}")
    return client

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


class TaskViewTests(APITestCase):
    def test_unauthenticated_user(self):
        client = APIClient()
        response = client.get("/tasks/")
        self.assertEqual(response.status_code, 401)

    def test_authenticated_user(self):
        client = get_authenticated_client()
        response = client.get("/tasks/")
        self.assertEqual(response.status_code, 200)

    def test_subtask_create_update_delete(self):
        client = get_authenticated_client()
        create_response = client.post(
            "/tasks/",
            {
                "title": "Test title",
                "description": "Test desc",
                "due_date": "2024-04-28",
                "assigned_to": 1,
                "subtasks": [
                    {
                        "title": "first subtask",
                        "completed": False
                    }
                ]
            },
            format="json"
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SubTask.objects.count(), 1)
        update_response = client.put(
            "/tasks/1/",
            {
                "title": "Test title",
                "description": "Test desc",
                "due_date": "2024-04-28",
                "assigned_to": 1,
                "subtasks": [
                    {
                        "id": 1,
                        "title": "first subtask",
                        "completed": True
                    },
                    {
                        
                        "title": "second subtask",
                        "completed": False
                    }
                ]
            },
            format="json"
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(SubTask.objects.get(pk=1).completed, True)
        self.assertEqual(SubTask.objects.count(), 2)
        delete_response = client.put(
            "/tasks/1/",
            {
                "title": "Test title",
                "description": "Test desc",
                "due_date": "2024-04-28",
                "assigned_to": 1,
                "subtasks": []
            },
            format="json"
        )
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        self.assertEqual(SubTask.objects.count(), 0)
