from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path('project/', views.ProjectList.as_view(), name='project_list'),
    path('project/<int:pk>', views.ProjectDetail.as_view(), name='project_list'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]