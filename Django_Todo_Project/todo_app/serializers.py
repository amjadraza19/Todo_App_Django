from rest_framework import serializers
from .models import TodoList


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoList
        fields = ['id', 'title', 'details', 'date', 'user']

