from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Task


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=4)

    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )


class TaskSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Task
        fields = ["id", "title", "description", "status",
                  "priority", "due_date", "created_date"]
        read_only_fields = ["id"]

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title is required")
        return value.strip()
