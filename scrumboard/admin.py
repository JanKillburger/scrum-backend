from django.contrib import admin
from scrumboard.models import Task

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    def save_model(self, request, task, form, change):
        if not task.pk: # checks for missing pk -> task is being created and user needs to be set
            task.created_by = request.user
        super().save_model(request, task, form, change)