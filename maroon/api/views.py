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
import json

class TokenAuthView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)


class ProfileCreate(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

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

    def put(self, request, *args, **kwargs):
        body = json.loads(request.body)

        project = None
        profile = models.Profile.objects.get(user=self.request.user)
        for user_project in profile.get_user_projects():
            if(user_project.pk == kwargs.get('pk')):
                project = user_project

        if not project:
            print("Not authorized")
            return Response("Project not found", status=status.HTTP_404_NOT_FOUND)
            
        project.name = body['name'];
        project.description = body['description'];
        #project.update_template(body['template'])
        #project.update_roles(body['roles'])
        project.save()
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
