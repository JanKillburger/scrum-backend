from rest_framework import viewsets
from scrumboard.models import Task
from scrumboard.serializers import TaskSerializer


# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
