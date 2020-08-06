from rest_framework import permissions
from task_management.models import Role, Profile, Project
from django.shortcuts import get_object_or_404


class ProjectAdmin(permissions.BasePermission):
    """
    Custom permissions to only allow admins of a project to access certain functionality
    """
    def has_permission(self, request, view):
        print("Getting permission")

        project = get_object_or_404(Project, pk=view.kwargs['pk'])
        profile = Profile.objects.get(user=request.user)
        if Role.objects.filter(profile=profile, project=project).exists():
            role = Role.objects.get(profile=profile, project=project)
            return role.role == "is_admin"
        return False

class ProjectCollaborator(permissions.BasePermission):
    """
    Custom permissions to only allow admins of a project to access certain functionality
    """
    def has_permission(self, request, view):
        #print(views.pretty_request(request))
        project = get_object_or_404(Project, pk=view.kwargs['pk'])
        #print(project)
        profile = Profile.objects.get(user=request.user)
        if Role.objects.filter(profile=profile, project=project).exists():
            role = Role.objects.get(profile=profile, project=project)
            return role.role == "is_normal" or role.role == "is_admin"
        return False