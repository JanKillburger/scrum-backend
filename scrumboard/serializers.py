from rest_framework import serializers
from . import models


class SubTaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = models.SubTask
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True)

    class Meta:
        model = models.Task
        fields = "__all__"

    def create(self, validated_data):
        subtasks_data = validated_data.pop("subtasks")
        task = models.Task.objects.create(**validated_data)
        for subtask_data in subtasks_data:
            models.SubTask.objects.create(task=task, **subtask_data)
        return task
    
    def update(self, instance, validated_data):
        new_subtasks_data = validated_data.pop("subtasks")
        self.handleSubtasks(instance, new_subtasks_data)
        super().update(instance, validated_data)
        return instance

    def handleSubtasks(self, task, validated_subtasks_data):
        db_subtasks = task.subtasks.all()
        request_ids = [subtask['id'] for subtask in validated_subtasks_data]
        data = {subtask['id']: subtask for subtask in validated_subtasks_data}
        for subtask in db_subtasks:
            if subtask.id not in request_ids:
                subtask.delete()
            else:
                subtask.title = data[subtask.id]['title']
                subtask.completed = data[subtask.id]['completed']
                subtask.save()

