from django.urls import path
from . import views

urlpatterns = [
    path('', views.Redirect.as_view()),
    path('landing', views.Landing.as_view(), name='landing'),

]