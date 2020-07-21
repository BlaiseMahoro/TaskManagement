from django.urls import path
from . import views

urlpatterns = [
    path('', views.Redirect.as_view()),
    path('landing', views.Landing.as_view(), name='landing'),
    path('account', views.Account.as_view(), name='account'),
    path('project', views.Project.as_view(), name='project'),
    path('register',  views.Register.as_view(), name = 'register'),
    path('avatar', views.UploadAvatar.as_view(), name = 'avatar')
]