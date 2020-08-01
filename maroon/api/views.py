from task_management import models
from api import serializers
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import authentication
from django.shortcuts import get_object_or_404
import json
from api.permissions import ProjectAdmin, ProjectCollaborator

class TokenAuthView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)


class ProfileCreate(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def post(self, request, format=None):
        body = json.loads(request.body)
        serializer = serializers.UserSerializer(data=body)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProfileDetail(TokenAuthView, generics.RetrieveUpdateDestroyAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def put(self, request, *args, **kwargs):
        body = json.loads(request.body)
        user = models.User.objects.get(username = request.user.username)
        serializer = serializers.UserSerializer(instance=user, data=body)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        user = models.User.objects.get(username = request.user.username)
        user.is_active = False
        user.save()
        return Response("Profile successfully deleted", status=status.HTTP_202_ACCEPTED)

    def get_object(self):
        return self.request.user
    
# For retrieving all projects and creating a project
class ProjectList(TokenAuthView, generics.ListCreateAPIView):
    serializer_class = serializers.ProjectSerializer
    queryset = models.Project.objects.all()

    def get_queryset(self):
        """
        This view should set the list of projects
        for the currently authenticated user.
        """ 
        return models.Profile.objects.get(user=self.request.user).get_user_projects()

    def post(self, request, format=None):
        #print(pretty_request(request))
        body = json.loads(request.body)

        project = models.Project(name=body['name'], description=body['description'])
        project.save(user=request.user)
        serializer = serializers.ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        

# For retrieving, updating, or detroying a project
class ProjectDetail(TokenAuthView, generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    permission_classes = [ProjectAdmin]

    def put(self, request, *args, **kwargs):
        body = json.loads(request.body)

        project = get_object_or_404(models.Project, pk=self.kwargs['pk'])

        if ProjectAdmin.has_object_permission(request, self, project):
            #Update Project details
            serializer = serializers.ProjectSerializer(project, data=body)
            serializer.is_valid()
            serializer.save()
            # Update Ticket Template
            template_serializer = serializers.TicketTemplateSerializer(instance=project.ticket_template, data=body['ticket_template'])
            template_serializer.is_valid()
            template_serializer.save()
            serializer.data.ticket_template = template_serializer.data
            # Update the roles
            serialized_roles = []
            for role in body['roles']:
                role_serializer = serializers.RoleSerializer(instance=project, data=role)
                role_serializer.is_valid()
                role_serializer.save()
                #serialized_roles.append({'role': role_serializer.validated_data['role'], 'username': role_serializer.validated_data['profile']})

            serializer.delete_removed_roles(project, body['roles'])
            #The roles data sent back is not getting assigned correctly
            #Don't this the following line works
            serializer.data['roles'] = role_serializer.data

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response("You do not have permission to update this project.", status=status.HTTP_403_FORBIDDEN)

# For retrieving all projects and creating a project
class TicketList(TokenAuthView, generics.ListCreateAPIView):
    serializer_class = serializers.TicketSerializer
    queryset = models.Ticket.objects.all()

    def get_queryset(self):
        """
        This view should set the list of projects
        for the currently authenticated user.
        """ 
        project = get_object_or_404(models.Project, pk=self.kwargs['pk'])
        print(models.Ticket.objects.filter(project=project))
        return models.Ticket.objects.filter(project=project)

    def post(self, request, format=None):
        #print(pretty_request(request))
        body = json.loads(request.body)

        project = models.Project(name=body['name'], description=body['description'])
        project.save(user=request.user)
        serializer = serializers.ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



    '''For printing post requests if needed.'''
def pretty_request(request):
    headers = ''
    for header, value in request.META.items():
        if not header.startswith('HTTP'):
            continue
        header = '-'.join([h.capitalize() for h in header[5:].lower().split('_')])
        headers += '{}: {}\n'.format(header, value)

    return (
        '{method} HTTP/1.1\n'
        'Content-Length: {content_length}\n'
        'Content-Type: {content_type}\n'
        '{headers}\n\n'
        '{body}'
    ).format(
        method=request.method,
        content_length=request.META['CONTENT_LENGTH'],
        content_type=request.META['CONTENT_TYPE'],
        headers=headers,
        body=request.body,
    )
