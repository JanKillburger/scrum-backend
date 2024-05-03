from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.forms import ValidationError
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from scrumboard.models import Task
from scrumboard.permissions import IsOwnerOrAssigneeOrReadonly, IsUserOrReadonly
from scrumboard.serializers import (
    TaskSerializer,
    UserSerializer,
    RegisterUserSerializer,
)


# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsOwnerOrAssigneeOrReadonly, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsUserOrReadonly, IsAuthenticated]


class RegisterUser(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # validate password with django built-in validators (requires User instance)
        user_to_validate = User(**serializer.validated_data)
        try:
            validate_password(user_to_validate.password, user_to_validate)
        except ValidationError as error:
            return Response({"password": error}, status=status.HTTP_400_BAD_REQUEST)
        # create user and user token and return it
        user = User.objects.create_user(**serializer.validated_data)
        token = Token.objects.create(user=user)
        response = {
            "username": user.username,
            "token": token.key
        }

        headers = self.get_success_headers(serializer.data)
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)
