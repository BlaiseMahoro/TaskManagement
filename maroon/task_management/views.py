from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, ListView, TemplateView, View
from django.views.generic.base import RedirectView
from django.http import HttpResponse
from .forms import RegisterForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class Redirect(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'landing'


class Landing(LoginRequiredMixin,View):  # Will later add: LoginRequredMixin
    login_url = 'login'
    template_name = "landing.html"

    def get(self, request):
        project = "Project one"
        project_2 = "Project two"
        context = {
            'some_value': project,
            'some_other_value': project_2,
        }
        return render(request, self.template_name, context)


class Account(LoginRequiredMixin,View):  # Will later add: LoginRequredMixin
    login_url = 'login'
    template_name = "user/account.html"

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class Register(View):
    template_name = "registration/register.html"

    def get(self, request):
        form = RegisterForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user) #authenticate user and redirect them to landing page
            return redirect('landing')
        context = {'form': form}
        return render(request, self.template_name, context)

