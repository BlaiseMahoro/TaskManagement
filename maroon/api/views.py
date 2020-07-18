from task_management import models
from api import serializers
from rest_framework import generics
from rest_framework import mixins

class ProfileCreate(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

# For retrieving all projects and creating a project
class ProjectList(generics.ListCreateAPIView):
    serializer_class = serializers.ProjectSerializer
    queryset = models.Project.objects.all()

    # def get_queryset(self):
    #     """
    #     This view should return a list of all the purchases
    #     for the currently authenticated user.
    #     """
        
    #     profile = models.Profile.objects.get(user=self.request.user)
    #     return models.Role.objects.filter(profile=profile).values('project')
    #     #return models..objects.all()

    # def post(self, request, format=None):
    #     serializer = ProjectSerializer(data=request.data)
    #     if serializer.is_valid():
            
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        role = Role()
        role.project = self.request.data
        serializer.save(owner=self.request.user)

# For retrieving, updating, or detroying a project
class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
