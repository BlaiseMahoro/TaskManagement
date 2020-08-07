from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path('project/', views.ProjectList.as_view(), name='project_list'),
    path('project/<int:pk>', views.ProjectDetail.as_view(), name='project_detail'),
    path('project/<int:pk>/ticket/', views.TicketList.as_view(), name='ticket_list'),
    path('project/<int:pk>/ticket/<int:ticket_pk>', views.TicketDetail.as_view(), name='ticket_detail'),
    path('profiles/', views.ProfileCreate.as_view(), name='profile_create'),
    path('profiles/myprofile/', views.ProfileDetail.as_view(), name='profile_update'),
    path('project/<int:pk>/ticket/<int:ticket_pk>/changestate', views.TicketUpdateState.as_view(), name='update_state'),
    path('project/<int:pk>/ticket/<int:ticket_pk>/comment', views.Comment.as_view(), name='comment'),
    path('project/<int:pk>/ticket/<int:ticket_pk>/comment/<int:comment_pk>', views.Comment.as_view(), name='comment'),
    path('project/<int:pk>/ticket/<int:ticket_pk>/link', views.Link.as_view(), name='link'),
    path('project/<int:pk>/ticket/<int:ticket_pk>/link/<int:link_pk>', views.Link.as_view(), name='comment'),
    path('project/<int:pk>/ticket/<int:ticket_pk>/file', views.File.as_view(), name='file'),
    path('project/<int:pk>/ticket/<int:ticket_pk>/file/<int:file_pk>', views.File.as_view(), name='comment'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]