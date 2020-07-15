from django.urls import path
from . import views

urlpatterns = [
    path('', views.Redirect.as_view()),
    path('landing', views.Landing.as_view(), name='landing'),
    path('account', views.Account.as_view(), name='account'),
    path('register',  views.Register.as_view(), name = 'register'),
]