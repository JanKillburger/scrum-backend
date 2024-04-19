from rest_framework import permissions

class IsOwnerOrAssignee(permissions.BasePermission):
    """Allow only owners and assignees of an object to edit it."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user in [obj.created_by, obj.assigned_to]