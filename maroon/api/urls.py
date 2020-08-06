from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path('project/', views.ProjectList.as_view(), name='project_list'),
    path('project/<int:pk>', views.ProjectDetail.as_view(), name='project_list'),
    path('profiles/', views.ProfileCreate.as_view(), name='profile_create'),
    path('profiles/myprofile/', views.ProfileDetail.as_view(), name='profile_update'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]