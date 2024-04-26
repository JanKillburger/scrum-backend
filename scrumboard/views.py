from django.contrib.auth.models import User
from rest_framework import viewsets
from scrumboard.models import Task
from scrumboard.permissions import IsOwnerOrAssigneeOrReadonly, IsUserOrReadonly
from scrumboard.serializers import TaskSerializer, UserSerializer


# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsOwnerOrAssigneeOrReadonly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsUserOrReadonly]
