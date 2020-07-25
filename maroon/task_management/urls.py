from django.urls import path
from . import views

urlpatterns = [
    path('', views.Redirect.as_view()),
    path('landing', views.LandingNoneSelected.as_view(), name='landingNoneSelected'),
    path('landing/<int:pk>', views.Landing.as_view(), name='landing'),
    path('account', views.Account.as_view(), name='account'),
    path('project', views.ProjectSettings.as_view(), name='project'),
    path('register',  views.Register.as_view(), name = 'register'),
    path('avatar', views.UploadAvatar.as_view(), name = 'avatar')
]