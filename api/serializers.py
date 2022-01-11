from todoapp.models import Todo
from rest_framework import serializers


class TodoSerializer(serializers.ModelSerializer):
    completed = serializers.ReadOnlyField()

    class Meta:
        model = Todo
        fields = ['id', 'title', 'important', 'created', 'completed']


class CompleteTodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = []
        read_only_fields = ['__all__']
