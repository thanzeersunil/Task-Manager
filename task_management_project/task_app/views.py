from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Task
from .serializers import RegisterSerializer, TaskSerializer
# Create your views here.


# Auth APIs
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful"},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"error": "Invalid username or password"},
                            status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)
        return Response({"message": "Login successful",
                         "token": token.key,
                         "username": user.username},
                        status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete() 
        return Response({"message": "Logged out"}, status=status.HTTP_200_OK)



# Task APIs
class TaskListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/tasks/  
    POST /api/tasks/ 
    """
    serializer_class = TaskSerializer

    def get_queryset(self):
        tasks = Task.objects.filter(user=self.request.user).order_by("-created_date")

        search = self.request.query_params.get("search")
        task_status = self.request.query_params.get("status")
        priority = self.request.query_params.get("priority")

        if search:
            tasks = tasks.filter(title__icontains=search)
        if task_status:
            tasks = tasks.filter(status=task_status)
        if priority:
            tasks = tasks.filter(priority=priority)

        return tasks

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/tasks/<id>/ 
    PUT    /api/tasks/<id>/  
    DELETE /api/tasks/<id>/ 
    """
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
