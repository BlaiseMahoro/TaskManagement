from rest_framework import permissions
from task_management.models import Role, Profile


class ProjectAdmin(permissions.BasePermission):
    """
    Custom permissions to only allow admins of a project to access certain functionality
    """
    def has_object_permission(request, view, obj):
        print("Getting permission")
        profile = Profile.objects.get(user=request.user)
        if Role.objects.filter(profile=profile, project=obj).exists():
            role = Role.objects.get(profile=profile, project=obj)
            return role.role == "is_admin"
        return False

class ProjectCollaborator(permissions.BasePermission):
    """
    Custom permissions to only allow admins of a project to access certain functionality
    """
    def has_object_permission(request, view, obj):
        profile = Profile.objects.get(user=request.user)
        if Role.objects.filter(profile=profile, project=obj).exists():
            role = Role.objects.get(profile=profile, project=obj)
            return role.role == "is_normal" or role.role == "is_admin"
        return False