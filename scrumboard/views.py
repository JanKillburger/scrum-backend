from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from scrumboard.models import Task
from scrumboard.serializers import TaskSerializer

# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class LoginView(ObtainAuthToken):
    permission_classes = []