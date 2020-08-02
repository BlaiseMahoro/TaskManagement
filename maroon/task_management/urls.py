from django.urls import path
from . import views

urlpatterns = [
    path('', views.Redirect.as_view()),
    path('landing', views.LandingNoneSelected.as_view(), name='landingNoneSelected'),
    path('landing/<int:pk>', views.Landing.as_view(), name='landing'),
    path('account', views.Account.as_view(), name='account'),
    path('project/<int:pk>', views.ProjectSettings.as_view(), name='project'),
    path('register',  views.Register.as_view(), name = 'register'),
    path('user/avatar', views.UploadAvatar.as_view(), name = 'user_avatar'),
    path('project/<int:pk>/avatar', views.UploadProjectAvatar.as_view(), name = 'project_avatar'),
    path('project/<int:pk>/create', views.CreateProject.as_view(), name='create_project_pk'), #pk in this url is for redirecting
    path('project/create', views.CreateProject.as_view(), name='create_project'), 
    path('delete', views.deleteuser, name='delete')  
]