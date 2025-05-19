import re
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers
from task_management.models import Task, SubTask, Category
from task_management.permissions.owner_permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User

class TaskCreateSerializer(serializers.ModelSerializer):
    deadline = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z")
    permission_classes = [IsOwnerOrReadOnly]
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline', 'owner']

    def validate_deadline(self, value: str):
        if value < timezone.now():
            raise serializers.ValidationError(
                {
                   "deadline": "Deadline cannot be in the past."
                }
            )
        return value


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline', 'owner']

class SubTaskSerializer(serializers.ModelSerializer):
    task = serializers.StringRelatedField()

    class Meta:
        model = SubTask
        fields = "__all__"


class TaskByIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TaskDetailSerializer(serializers.ModelSerializer):
    subtask_set = SubTaskSerializer(many=True)
    permission_classes = [IsOwnerOrReadOnly]

    class Meta:
        model = Task
        fields = "__all__"


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    permission_classes = [IsOwnerOrReadOnly]

    class Meta:
        model = SubTask
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

    def validate_name(self, value: str):
        if value:
            exists_name = Category.objects.filter(name__iexact=value).exists()
            if exists_name:
                raise serializers.ValidationError(
                    {
                        "name": "Category with this name already exists"
                    }
                )
        return value

    def create(self, validated_data: dict[str, str | int | float]) -> Category:
        return super().create(validated_data)

    def update(self, instance: Category, validated_data: dict[str, str | int | float]) -> Category:
        return super().update(instance, validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'first_name',
            'last_name', 'password',
            're_password', 'email',
        ]

    def validate(self, attrs):
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')

        re_pattern = r'^[a-zA-Z]+$'

        if not re.match(re_pattern, first_name):
            raise serializers.ValidationError(
                {"first_name": "First name must contain only alphabet characters."}
            )

        if not re.match(re_pattern, last_name):
            raise serializers.ValidationError(
                {"last_name": "Last name must contain only alphabet characters."}
            )

        password = attrs.get('password')
        re_password = attrs.pop('re_password', None)

        if not password:
            raise serializers.ValidationError(
                {"password": "This field is Required"}
            )

        if not re_password:
            raise serializers.ValidationError(
                {"re_password": "This field is Required"}
            )

        validate_password(password)

        if password != re_password:
            raise serializers.ValidationError(
                {"re_password": "Password did not match."}
            )
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)

        user.save()

        return user

