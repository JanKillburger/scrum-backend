from django.contrib.auth.models import User
from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "id"]

class SubTaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = models.SubTask
        fields = "__all__"

class TaskResponseSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True)
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)

    class Meta:
        model = models.Task
        fields = "__all__"

class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, required=False)
    
    class Meta:
        model = models.Task
        fields = "__all__"

    def to_representation(self, instance):
        return TaskResponseSerializer(context=self.context).to_representation(instance)

    def create(self, validated_data):
        print(validated_data)
        if "subtasks" in validated_data.keys():
            subtasks_data = validated_data.pop("subtasks")
        task = models.Task.objects.create(**validated_data)
        if subtasks_data:
            for subtask_data in subtasks_data:
                models.SubTask.objects.create(task=task, **subtask_data)
        return task

    def update(self, instance, validated_data):
        if "subtasks" in validated_data.keys():
            subtasks_data = validated_data.pop("subtasks")
            self.handle_subtasks(instance, subtasks_data)
        super().update(instance, validated_data)
        return instance

    def handle_subtasks(self, task, validated_subtasks_data):
        """Create, update and delete subtasks.
        
            Create new subtask if 'id' key is not provided.
            Update subtasks for which 'id' key is provided.
            Delete subtasks if they are not provided."""
        db_subtasks = task.subtasks.all()
        items_to_update = {}
        items_to_create = []
        for validated_subtask_data in validated_subtasks_data:
            if "id" in validated_subtask_data.keys():
                items_to_update[validated_subtask_data["id"]] = validated_subtask_data
            else:
                items_to_create.append(validated_subtask_data)

        for subtask in db_subtasks:
            if subtask.id in items_to_update.keys():
                models.SubTask.objects.filter(id=subtask.id).update(
                    **items_to_update[subtask.id]
                )
            else:
                subtask.delete()

        for subtask in items_to_create:
            models.SubTask.objects.create(task=task, **subtask)
